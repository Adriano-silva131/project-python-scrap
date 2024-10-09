from sqlalchemy.orm import sessionmaker
from config import engine
from data import get_file_paths, extract_data_from_file, insert_data_to_db
from config import DIRECTORY_PATH

def main():

    Session = sessionmaker(bind=engine)
    db = Session()
    
    file_paths = get_file_paths(DIRECTORY_PATH)
    all_data = []
    
    for file_path in file_paths:
        extracted_data = extract_data_from_file(file_path)
        all_data.extend(extracted_data)
    
    insert_data_to_db(db, all_data)
    print("Dados importados com sucesso!")

if __name__ == "__main__":
    main()
