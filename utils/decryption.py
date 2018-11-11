"""
This is a copy of: sqlalchemy_utils.types.encrypted.encrypted_type.AesEngine
from the sqlalchemy-utils library.
The aim is to be able to decrypt an EncryptedType column (so a column
that was encrypted using SQLAlchemy).

Note: the sqlalchemy-utils library has a dependency on the full sqlalchemy library
itself, thus I chose to copy this code rather then adding too many requirements.

It requires the library cryptography

Usage:
engine = AesEngine()
engine._set_padding_mechanism(None)
engine._update_key(settings.ORCID_TOKENS_ENCRYPTION_KEY)
engine.decrypt(RemoteToken.objects.all()[0].access_token)
"""
import base64
import six

cryptography = None
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)


class InvalidCiphertextError(Exception):
    pass


class EncryptionDecryptionBaseEngine(object):
    """A base encryption and decryption engine.

    This class must be sub-classed in order to create
    new engines.
    """

    def _update_key(self, key):
        if isinstance(key, six.string_types):
            key = key.encode()
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(key)
        engine_key = digest.finalize()

        self._initialize_engine(engine_key)

    def encrypt(self, value):
        raise NotImplementedError('Subclasses must implement this!')

    def decrypt(self, value):
        raise NotImplementedError('Subclasses must implement this!')


class AesEngine(EncryptionDecryptionBaseEngine):
    """Provide AES encryption and decryption methods.

    You may also consider using the AesGcmEngine instead -- that may be
    a better fit for some cases.

    You should NOT use the AesGcmEngine if you want to be able to search
    for a row based on the value of an encrypted column. Use AesEngine
    instead, since that allows you to perform such searches.

    If you don't need to search by the value of an encypted column, the
    AesGcmEngine provides better security.
    """

    BLOCK_SIZE = 16

    def _initialize_engine(self, parent_class_key):
        self.secret_key = parent_class_key
        self.iv = self.secret_key[:16]
        self.cipher = Cipher(
            algorithms.AES(self.secret_key),
            modes.CBC(self.iv),
            backend=default_backend()
        )

    def _set_padding_mechanism(self, padding_mechanism=None):
        """Set the padding mechanism."""
        if isinstance(padding_mechanism, six.string_types):
            if padding_mechanism not in PADDING_MECHANISM.keys():
                raise Exception(
                    "There is not padding mechanism with name {}".format(
                        padding_mechanism
                    )
                )

        if padding_mechanism is None:
            padding_mechanism = 'naive'

        padding_class = PADDING_MECHANISM[padding_mechanism]
        self.padding_engine = padding_class(self.BLOCK_SIZE)

    def encrypt(self, value):
        if not isinstance(value, six.string_types):
            value = repr(value)
        if isinstance(value, six.text_type):
            value = str(value)
        value = value.encode()
        value = self.padding_engine.pad(value)
        encryptor = self.cipher.encryptor()
        encrypted = encryptor.update(value) + encryptor.finalize()
        encrypted = base64.b64encode(encrypted)
        return encrypted

    def decrypt(self, value):
        if isinstance(value, six.text_type):
            value = str(value)
        decryptor = self.cipher.decryptor()
        decrypted = base64.b64decode(value)
        decrypted = decryptor.update(decrypted) + decryptor.finalize()
        decrypted = self.padding_engine.unpad(decrypted)
        if not isinstance(decrypted, six.string_types):
            try:
                decrypted = decrypted.decode('utf-8')
            except UnicodeDecodeError:
                raise ValueError('Invalid decryption key')
        return decrypted


class InvalidPaddingError(Exception):
    pass


class Padding(object):
    """Base class for padding and unpadding."""

    def __init__(self, block_size):
        self.block_size = block_size

    def pad(value):
        raise NotImplementedError('Subclasses must implement this!')

    def unpad(value):
        raise NotImplementedError('Subclasses must implement this!')


class PKCS5Padding(Padding):
    """Provide PKCS5 padding and unpadding."""

    def pad(self, value):
        if not isinstance(value, six.binary_type):
            value = value.encode()
        padding_length = (self.block_size - len(value) % self.block_size)
        padding_sequence = padding_length * six.b(chr(padding_length))
        value_with_padding = value + padding_sequence

        return value_with_padding

    def unpad(self, value):
        # Perform some input validations.
        # In case of error, we throw a generic InvalidPaddingError()
        if not value or len(value) < self.block_size:
            # PKCS5 padded output will always be at least 1 block size
            raise InvalidPaddingError()
        if len(value) % self.block_size != 0:
            # PKCS5 padded output will be a multiple of the block size
            raise InvalidPaddingError()
        if isinstance(value, six.binary_type):
            padding_length = value[-1]
        if isinstance(value, six.string_types):
            padding_length = ord(value[-1])
        if padding_length == 0 or padding_length > self.block_size:
            raise InvalidPaddingError()

        def convert_byte_or_char_to_number(x):
            return ord(x) if isinstance(x, six.string_types) else x
        if any([padding_length != convert_byte_or_char_to_number(x)
               for x in value[-padding_length:]]):
            raise InvalidPaddingError()

        value_without_padding = value[0:-padding_length]

        return value_without_padding


class OneAndZeroesPadding(Padding):
    """Provide the one and zeroes padding and unpadding.

    This mechanism pads with 0x80 followed by zero bytes.
    For unpadding it strips off all trailing zero bytes and the 0x80 byte.
    """

    BYTE_80 = 0x80
    BYTE_00 = 0x00

    def pad(self, value):
        if not isinstance(value, six.binary_type):
            value = value.encode()
        padding_length = (self.block_size - len(value) % self.block_size)
        one_part_bytes = six.b(chr(self.BYTE_80))
        zeroes_part_bytes = (padding_length - 1) * six.b(chr(self.BYTE_00))
        padding_sequence = one_part_bytes + zeroes_part_bytes
        value_with_padding = value + padding_sequence

        return value_with_padding

    def unpad(self, value):
        value_without_padding = value.rstrip(six.b(chr(self.BYTE_00)))
        value_without_padding = value_without_padding.rstrip(
            six.b(chr(self.BYTE_80)))

        return value_without_padding


class ZeroesPadding(Padding):
    """Provide zeroes padding and unpadding.

    This mechanism pads with 0x00 except the last byte equals
    to the padding length. For unpadding it reads the last byte
    and strips off that many bytes.
    """

    BYTE_00 = 0x00

    def pad(self, value):
        if not isinstance(value, six.binary_type):
            value = value.encode()
        padding_length = (self.block_size - len(value) % self.block_size)
        zeroes_part_bytes = (padding_length - 1) * six.b(chr(self.BYTE_00))
        last_part_bytes = six.b(chr(padding_length))
        padding_sequence = zeroes_part_bytes + last_part_bytes
        value_with_padding = value + padding_sequence

        return value_with_padding

    def unpad(self, value):
        if isinstance(value, six.binary_type):
            padding_length = value[-1]
        if isinstance(value, six.string_types):
            padding_length = ord(value[-1])
        value_without_padding = value[0:-padding_length]

        return value_without_padding


class NaivePadding(Padding):
    """Naive padding and unpadding using '*'.

    The class is provided only for backwards compatibility.
    """

    CHARACTER = six.b('*')

    def pad(self, value):
        num_of_bytes = (self.block_size - len(value) % self.block_size)
        value_with_padding = value + num_of_bytes * self.CHARACTER

        return value_with_padding

    def unpad(self, value):
        value_without_padding = value.rstrip(self.CHARACTER)

        return value_without_padding


PADDING_MECHANISM = {
    'pkcs5': PKCS5Padding,
    'oneandzeroes': OneAndZeroesPadding,
    'zeroes': ZeroesPadding,
    'naive': NaivePadding
}