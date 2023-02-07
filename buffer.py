class Buffer:
    """!The Buffer class.
    Produces the Abstract Syntax Tree from C/C++ language source code.
    """

    @staticmethod
    def load_buffer(path_file: str):
        """! Load file content.
        @param path_file  The input file path.
        @return
        """
        arq = open(path_file, 'r')
        text = arq.readline()

        buffer = []
        cont = 1

        # The buffer size can be changed by changing cont
        while text != "":
            buffer.append(text)
            text = arq.readline()
            cont += 1

            if cont == 10 or text == '':
                # Return a full buffer
                buf = ''.join(buffer)
                cont = 1
                yield buf

                # Reset the buffer
                buffer = []

        arq.close()
