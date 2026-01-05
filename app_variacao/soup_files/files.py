"""
    Esté módulo serve para manipulação de arquivos, diretórios e documentos
entre outros. Não depende de módulos externos apenas de builtins e stdlib.
"""
from __future__ import annotations
from typing import Any
from enum import Enum
import os
import json
import platform
from hashlib import md5

# Windows / Linux / ...
KERNEL_TYPE = platform.system()


class ExtensionFiles(Enum):

    PNG = '.png'
    JPG = '.jpg'
    JPEG = '.jpeg'
    SVG = '.svg'
    PDF = '.pdf'
    XLSX = '.xlsx'
    XLS = '.xls'
    CSV = '.csv'
    TXT = '.txt'
    ODS = '.ods'
    JSON = '.json'


class EnumDocFiles(Enum):
    """
        Enum para tipos de documentos como imagens, PDFs, Planilhas e JSON.
    """

    IMAGE = ['.png', '.jpg', '.jpeg', '.svg']
    PDF = ['.pdf']
    DOCUMENTS = ['.png', '.jpg', '.jpeg', '.svg', '.pdf']
    #
    EXCEL = ['.xlsx', '.xls']
    CSV = ['.csv', '.txt']
    ODS = ['.ods']
    #
    SHEET = ['.csv', '.txt', '.xlsx', '.xls', '.ods']
    JSON = ['.json']
    #
    ALL_DOCUMENTS = [
        '.png', '.jpg', '.jpeg', '.svg',
        '.csv', '.txt', '.xlsx', '.xls', '.ods',
        '.pdf',
        '.json',
        '.zip',
        '.*'
    ]
    #
    ALL = "ALL"

    @property
    def values(self) -> list[str]:
        return [
        '.png', '.jpg', '.jpeg', '.svg',
        '.csv', '.txt', '.xlsx', '.xls', '.ods',
        '.pdf',
        '.json',
        '.zip',
        '.*'
    ]


class File(object):
    def __init__(self, filename: str):
        if os.path.isdir(filename):
            raise ValueError(f'{__class__.__name__} File() não pode ser um diretório.')
        self._abs_filename: str = os.path.abspath(filename)

    def __repr__(self):
        return f'{__class__.__name__}() {self.extension()} => {self.absolute()}'

    def __eq__(self, value: File):
        if not isinstance(value, File):
            return ValueError()
        return self.absolute() == value.absolute()

    def __hash__(self):
        return self.absolute().__hash__()

    def is_image(self) -> bool:
        try:
            return True if self.extension() in EnumDocFiles.IMAGE.value else False
        except:
            return False

    def is_pdf(self) -> bool:
        try:
            return True if self.extension() in EnumDocFiles.PDF.value else False
        except:
            return False

    def is_excel(self) -> bool:
        try:
            return True if self.extension() in EnumDocFiles.EXCEL.value else False
        except:
            return False

    def is_csv(self) -> bool:
        try:
            return True if self.extension() in EnumDocFiles.CSV.value else False
        except:
            return False

    def is_sheet(self) -> bool:
        try:
            return True if self.extension() in EnumDocFiles.SHEET.value else False
        except:
            return False

    def is_json(self) -> bool:
        try:
            return True if self.extension() in EnumDocFiles.JSON.value else False
        except:
            return False

    def is_ods(self):
        try:
            return True if self.extension() in EnumDocFiles.ODS.value else False
        except:
            return False

    def update_extension(self, e: str) -> File:
        """
            Retorna uma instância de File() no mesmo diretório com a nova
        extensão informada.
        """
        current = self.extension()
        full_path = self.absolute().replace(current, '')
        return File(os.path.join(f'{full_path}{e}'))

    def get_text(self) -> str | None:
        try:
            with open(self.absolute(), 'rt') as fp:
                return fp.read()
        except Exception as e:
            print(f'{__class__.__name__} {e}')
            return None

    def write_string(self, s: str) -> bool:
        try:
            # Definir encoding é essencial para evitar bugs silenciosos
            with open(self.absolute(), mode='a', encoding='utf-8') as fp:
                fp.write(s)
        except OSError as e:
            # self.__class__.__name__ garante o nome correto da classe atual
            print(f"[{self.__class__.__name__}] Erro ao escrever no arquivo: {e}")
            return False
        return True

    def write_list(self, items: list[str]) -> bool:
        if len(items) == 0:
            return False
        try:
            with open(self.absolute(), "w", encoding="utf-8") as file:
                for string in items:
                    file.write(string + "\n")
        except Exception as e:
            print(e)
            return False
        else:
            return True

    def name(self):
        e = self.extension()
        if (e is None) or (e == ''):
            return os.path.basename(self._abs_filename)
        return os.path.basename(self._abs_filename).replace(e, '')

    def name_absolute(self) -> str:
        e = self.extension()
        if (e is None) or (e == ''):
            return self._abs_filename
        return self._abs_filename.replace(e, '')

    def extension(self) -> str | None:
        try:
            return os.path.splitext(self.absolute())[1]
        except:
            return None

    def dirname(self) -> str:
        return os.path.dirname(self._abs_filename)

    def basename(self) -> str:
        return os.path.basename(self._abs_filename)

    def exists(self) -> bool:
        return os.path.exists(self.absolute())

    def absolute(self) -> str:
        return self._abs_filename

    def size(self):
        return os.path.getsize(self._abs_filename)

    def md5(self) -> str | None:
        """Retorna a hash md5 de um arquivo se ele existir no disco."""
        if not self.exists():
            return None
        _hash_md5 = md5()
        with open(self.absolute(), "rb") as f:
            for _block in iter(lambda: f.read(4096), b""):
                _hash_md5.update(_block)
        return _hash_md5.hexdigest()


class Directory(object):
    def __init__(self, dirpath: str):
        self.__abs_path: str = os.path.abspath(dirpath)

    def absolute(self) -> str:
        return self.__abs_path

    def __repr__(self):
        return f'{__class__.__name__}: {self.absolute()}'

    def __eq__(self, value):
        if not isinstance(value, Directory):
            return ValueError()
        return self.absolute() == value.absolute()

    def __hash__(self):
        return self.absolute().__hash__()

    def get_files(self) -> list[str]:
        """
        Retorna a lista de diretórios e sub pastas.
        """
        path_list = []
        # os.walk percorre a árvore de diretórios recursivamente
        for root, dirs, files in os.walk(self.absolute()):
            # Adiciona os diretórios encontrados
            for name in dirs:
                path_list.append(os.path.join(root, name))
            # Adiciona os arquivos encontrados
            for name in files:
                path_list.append(os.path.join(root, name))
        return path_list

    def __content_recursive(self) -> list[File]:
        _paths: list[str] = self.get_files()
        values: list[File] = []
        for file_path in _paths:
            if os.path.isfile(file_path):
                values.append(
                    File(os.path.abspath(file_path))
                )
        return values

    def __content_no_recursive(self) -> list[File]:
        content_files: list[str] = os.listdir(self.absolute())
        values: list[File] = []
        for file in content_files:
            fp: str = os.path.join(self.absolute(), file)
            if os.path.isfile(fp):
                values.append(
                    File(os.path.abspath(fp))
                )
        return values

    def content_files(self, *, recursive: bool = True) -> list[File]:
        if recursive:
            return self.__content_recursive()
        return self.__content_no_recursive()

    def content_dirs(self, recursive: bool = True) -> list[Directory]:
        """
        retorna uma lista de diretórios
        """
        values: list[Directory] = []
        if recursive:
            _paths = self.get_files()
            for p in _paths:
                if os.path.isdir(p):
                    values.append(
                        Directory(os.path.abspath(p))
                    )
        else:
            _paths = os.listdir(self.absolute())
            for d in _paths:
                _dirpath = os.path.join(self.absolute(), d)
                if os.path.isdir(_dirpath):
                    values.append(
                        Directory(os.path.abspath(_dirpath))
                    )
        return values

    def basename(self) -> str:
        return os.path.basename(self.absolute())

    def mkdir(self):
        try:
            os.makedirs(self.absolute())
        except:
            pass

    def concat(self, d: str, create: bool = False) -> Directory:
        if create:
            if not os.path.exists(os.path.join(self.absolute(), d)):
                try:
                    os.makedirs(os.path.join(self.absolute(), d))
                except Exception as err:
                    print(err)
        return Directory(os.path.join(self.absolute(), d))

    def parent(self) -> Directory:
        return Directory(
            os.path.abspath(os.path.dirname(self.absolute()))
        )

    def join_file(self, name: str) -> File:
        return File(
            os.path.join(self.absolute(), name)
        )


class ContentFiles(object):
    """
        Obter uma lista de arquivos/documentos do diretório informado.
    """

    def __init__(self, d: Directory, *, max_files: int = 5000):
        if not isinstance(d, Directory):
            raise ValueError(f'{__class__.__name__}\nUse: Directory(), não {type(d)}')
        self._input_dir: Directory = d
        self.__max_files: int = max_files

    def get_images(self) -> list[File]:
        return self.get_files(file_type=EnumDocFiles.IMAGE)

    def get_pdfs(self) -> list[File]:
        return self.get_files(file_type=EnumDocFiles.PDF)

    def get_sheets(self) -> list[File]:
        return self.get_files(file_type=EnumDocFiles.SHEET)

    def get_files_with(self, *, infile: str, sort: bool = True) -> list[File]:
        """
            Retorna arquivos que contém a ocorrência (infile) no nome absoluto.
        """
        content_files: list[File] = []
        count: int = 0
        paths: list[str] = self._input_dir.get_files()
        file: str
        for file in paths:
            if not os.path.isfile(file):
                continue
            if infile in os.path.abspath(file):
                content_files.append(
                    File(os.path.abspath(file))
                )
                count += 1
            if count >= self.__max_files:
                break
        if sort:
            content_files.sort()
        return content_files

    def __get_files_recursive(self, *, file_type: EnumDocFiles, sort: bool) -> list[File]:
        #
        _paths: list[str] = self._input_dir.get_files()
        _all_files: list[File] = list()
        count: int = 0
        if file_type == EnumDocFiles.ALL:
            # Todos os tipos de arquivos
            for p in _paths:
                if not os.path.isfile(p):
                    continue
                _all_files.append(
                    File(os.path.abspath(p))
                )
                count += 1
                if count >= self.__max_files:
                    break
        else:
            # Arquivos especificados em LibraryDocs
            for p in _paths:
                if not os.path.isfile(p):
                    continue

                file_suffix = os.path.splitext(p)[1]
                if (file_suffix is None) or (file_suffix == ''):
                    continue
                if file_suffix in file_type.value:
                    _all_files.append(
                        File(os.path.abspath(p))
                    )
                    count += 1
                if count >= self.__max_files:
                    break
        if sort:
            _all_files.sort(key=File.absolute)
        return _all_files

    def __get_files_no_recursive(self, *, file_type: EnumDocFiles, sort: bool) -> list[File]:
        _content_files: list[File] = self._input_dir.content_files(recursive=False)
        _all_files: list[File] = []
        count: int = 0

        if file_type == EnumDocFiles.ALL:
            # Todos os tipos de arquivos
            for file in _content_files:
                _all_files.append(file)
                count += 1
                if count == self.__max_files:
                    break
        else:
            # Arquivos especificados em LibraryDocs
            for file in _content_files:
                if file.extension() in file_type.value:
                    _all_files.append(file)
                    count += 1
                    if count == self.__max_files:
                        break
        if sort:
            _all_files.sort(key=File.absolute)
        return _all_files

    def get_files(
            self, *,
            file_type: EnumDocFiles = EnumDocFiles.ALL_DOCUMENTS,
            sort: bool = True,
            recursive: bool = True
    ) -> list[File]:
        """
            Retorna uma lista de File() conforme o tipo de arquivo
        especificado.
        - LibraryDocs.ALL_DOCUMENTS => Retorna todos os documentos do diretório.
        - LibraryDocs.EXCEL         => Retorna arquivos que são planilhas excel.
        - ...
        
        """
        if recursive:
            return self.__get_files_recursive(file_type=file_type, sort=sort)
        return self.__get_files_no_recursive(file_type=file_type, sort=sort)


class JsonData(object):
    """
        Representação de um dado JSON apartir de uma string python.
    """

    def __init__(self, string: str):
        if not isinstance(string, str):
            raise ValueError(f'{__class__.__name__} o JSON informado precisa ser do tipo string, não {type(string)}')
        self.jsonString: str = string

    def is_null(self) -> bool:
        if (self.jsonString is None) or (self.jsonString == ''):
            return True
        return False

    def to_string(self) -> str:
        return self.jsonString

    def to_dict(self) -> dict[str, Any]:
        """
            Exportar/Converter o dado atual em um dicionário python.
        """
        return json.loads(self.jsonString)

    def to_file(self, f: File):
        """Exportar o dado atual para um arquivo .json"""
        _data: str = json.loads(self.jsonString)
        with open(f.absolute(), "w", encoding="utf-8") as file:
            json.dump(_data, file, indent=4, ensure_ascii=False)


class JsonConvert(object):
    """
        Conversão de um dado JSON em dados python
    """

    def __init__(self, data: JsonData):
        self.data: JsonData = data

    def to_json_data(self) -> JsonData:
        return self.data

    @classmethod
    def from_file(cls, file: File) -> JsonConvert:
        """
            Gerar um dado JsonData apartir de arquivo .json
        """
        # Ler o arquivo e carregar o JSON em um dicionário Python
        data = None
        try:
            with open(file.absolute(), "r", encoding="utf-8") as fp:
                data: str = json.load(fp)
        except Exception as e:
            print(f'{__class__.__name__}\n{e}')
            return cls(JsonData(''))
        else:
            return cls(JsonData(json.dumps(data, indent=4, ensure_ascii=False, sort_keys=True)))

    @classmethod
    def from_string_json(cls, data: str) -> JsonConvert:
        """
            Gerar um dado JsonData apartir de uma string.
        """
        json_string = json.dumps(data, indent=4, ensure_ascii=False, sort_keys=True)
        return cls(JsonData(json_string))

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> JsonConvert:
        """
            Converte um dicionário em objeto JSON/JsonData.
        """
        if not isinstance(data, dict):
            raise ValueError(f'{__class__.__name__} Informe um JSON em formato dict, não {type(data)}')
        json_string = json.dumps(data, indent=4, ensure_ascii=False, sort_keys=True)
        return cls(JsonData(json_string))


class UserFileSystem(object):
    """
        Diretórios comuns para cache e configurações de usuário.
    """

    def __init__(self, base_home: Directory = None):
        self.__base_home: Directory | None = base_home
        if self.__base_home is None:
            # _home = Directory(os.path.expanduser("~"))
            # HOME (Unix) / USERPROFILE (Windows)
            _home = os.environ.get('HOME') or os.environ.get('USERPROFILE')
            if _home is None or _home == "":
                _home = Directory(os.path.expanduser("~"))
            self.__base_home = Directory(_home)
        self.__user_downloads: Directory = self.__base_home.concat('Downloads', create=True)
        self.__user_var_dir: Directory = self.__base_home.concat('var', create=True)

    def __repr__(self):
        return f'{__class__.__name__}(): Home {self.get_user_home()}'

    def get_user_dir_var(self) -> Directory:
        return self.__user_var_dir

    def set_user_dir_var(self, d: Directory) -> None:
        self.__user_var_dir = d

    def get_user_downloads(self) -> Directory:
        return self.__user_downloads

    def set_user_downloads(self, d: Directory) -> None:
        self.__user_downloads = d

    def get_user_home(self) -> Directory | None:
        return self.__base_home

    def set_user_home(self, d: Directory) -> None:
        self.__base_home = d

    def config_dir(self) -> Directory:
        return self.__user_var_dir.concat('config', create=True)

    def cache_dir(self) -> Directory:
        return self.__user_var_dir.concat('cache', create=True)


class UserAppDir(object):
    """
        Diretório comun para cache e configurações do aplicativo.
    """

    def __init__(self, appname: str, *, user_file_system: UserFileSystem = UserFileSystem()):
        self.appname = appname
        self.userFileSystem: UserFileSystem = user_file_system
        self.workspaceDirApp = self.userFileSystem.get_user_downloads().concat(self.appname, create=False)
        self.installDir = self.userFileSystem.get_user_dir_var().concat('opt').concat(self.appname, create=False)

    def cache_dir_app(self) -> Directory:
        return self.userFileSystem.cache_dir().concat(self.appname, create=False)

    def config_dir_app(self) -> Directory:
        return self.userFileSystem.config_dir().concat(self.appname, create=False)
