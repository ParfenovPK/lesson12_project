import os
import random

from loader.exceptions import PictureFormatNotSupportedError, PictureNotUploadedError, OutOfFreeNamesError


class UploadManager:

    def get_free_filename(self, folder, file_type):
        attemps = 0
        RANGE_OF_IMAGE_NUMBERS = 100
        LIMIT_OF_ATTEMPS = 1000

        while True:
            pic_name = str(random.randint(0, RANGE_OF_IMAGE_NUMBERS))
            filename_to_save = f'{pic_name}.{file_type}'
            os_path = os.path .join(folder, filename_to_save)
            is_filename_occupied = os.path.exists(os_path)

            if not is_filename_occupied:
                return filename_to_save

            attemps += 1

            if attemps > LIMIT_OF_ATTEMPS:
                raise OutOfFreeNamesError("No free names to save Image")

    def is_file_type_velid(self, file_type):
        if file_type.lower() in ['jpg', 'jpeg', 'gif', 'png', 'webp', 'tiff']:
            return True
        return False

    def save_with_random_name(self, picture):

        # Получаем данные  с картинкой
        filename = picture.filename
        file_type = filename.split('.')[-1]

        # Проверяем видимость картинки

        if not self.is_file_type_velid(file_type):
            raise PictureFormatNotSupportedError(f'Формат {file_type} не поддерживается')

        # Получаем свободное имя
        folder = os.path.join('.', 'uploads', 'images')
        filename_to_save = self.get_free_filename(folder, file_type)

        # Сохраянем под новым именем
        try:
            picture.save(os.path.join(folder, filename_to_save))
        except FileNotFoundError:
            raise PictureNotUploadedError(f"{folder, filename_to_save}")

        return filename_to_save


