import ftplib
import ssl

import logging
from typing import Any, BinaryIO


class ImplicitFTP_TLS(ftplib.FTP_TLS):
    """FTP_TLS subclass that automatically wraps sockets in SSL to support implicit FTPS."""  # noqa

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sock = None

    @property
    def sock(self):
        """Return the socket."""
        return self._sock

    @sock.setter
    def sock(self, value):
        """When modifying the socket, ensure that it is ssl wrapped."""
        if value is not None and not isinstance(value, ssl.SSLSocket):
            value = self.context.wrap_socket(value)
        self._sock = value

    def storbinary(self, cmd, fp, blocksize=8192, callback=None, rest=None):
        self.voidcmd('TYPE I')
        conn = self.transfercmd(cmd, rest)
        try:
            while 1:
                buf = fp.read(blocksize)
                if not buf:
                    break
                conn.sendall(buf)
                if callback:
                    callback(buf)
            # shutdown ssl layer
            if isinstance(conn, ssl.SSLSocket):
                # conn.unwrap()  # Fix for storbinary waiting indefinitely for response message from server  # noqa
                pass
        finally:
            conn.close()  # This is the addition to the previous comment.
        return self.voidresp()


class PrinterFTPClient:
    def __init__(self,
                 server_ip: str,
                 access_code: str,
                 user: str = 'bblp',
                 port: int = 990) -> None:
        self.ftps = ImplicitFTP_TLS()

        self.server_ip = server_ip
        self.port = port
        self.user = user
        self.access_code = access_code

    @staticmethod
    def connect_and_run(func):
        """
        A decorator that connects to the FTP server before running the function and closes the connection after running the function.

        Args:
            func (function): the function to be decorated
        """ # noqa
        def wrapper(self, *args, **kwargs) -> Any:
            logging.info("Connecting to FTP server...")
            self.ftps.connect(host=self.server_ip, port=self.port)
            self.ftps.login(self.user, self.access_code)
            logging.info("Connected to FTP server")
            logging.info(self.ftps.prot_p())

            try:
                return func(self, *args, **kwargs)  # type: ignore
            except Exception as e:                                  # noqa  # pylint: disable=broad-exception-caught
                logging.error(f"Failed to execute function: {e}")   # noqa  # pylint: disable=logging-fstring-interpolation
            finally:
                self.ftps.close()
                logging.info("Connection to FTP server closed")
        return wrapper

    @connect_and_run
    def upload_file(self, file: BinaryIO, file_path: str) -> str:
        return self.ftps.storbinary(f'STOR {file_path}', file, blocksize=32768,
                                 callback=lambda x: logging.debug(f"Uploaded {x} bytes"))   # noqa  # pylint: disable=logging-fstring-interpolation

    @connect_and_run
    def delete_file(self, file_path: str) -> str:
        logging.info(f"Deleting file: {file_path}")     # noqa  # pylint: disable=logging-fstring-interpolation
        return self.ftps.delete(file_path)

    def close(self) -> None:
        self.ftps.quit()
