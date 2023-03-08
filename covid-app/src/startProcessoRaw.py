
from carga.processaCovidRaw import processaCovidRaw
def startProcess():
    try:
        print("Carga de arquivos csv do site do governo.")
        execute = processaCovidRaw()
        execute.main()

    except Exception as e:
        print("Erro executing startProcess")
        print(str(e))
        raise

if __name__ == "__main__":
    startProcess()