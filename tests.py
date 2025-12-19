import pytest
from main import BooksCollector


class TestBooksCollector:

    # ---------- add_new_book ----------

    def test_add_new_book_adds_two_different_books(self):
        # создаем экземпляр класса BooksCollector
        collector = BooksCollector()

        # добавляем две разные книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что в словаре появилось две книги
        assert len(collector.get_books_genre()) == 2

    def test_add_new_book_does_not_add_duplicate_book(self):
        # создаем экземпляр класса BooksCollector
        collector = BooksCollector()

        # дважды добавляем одну и ту же книгу
        collector.add_new_book('Дюна')
        collector.add_new_book('Дюна')

        # проверяем, что книга добавлена только один раз
        assert len(collector.get_books_genre()) == 1

    def test_add_new_book_with_empty_name_does_not_add_book(self):
        # создаем экземпляр класса BooksCollector
        collector = BooksCollector()

        # пытаемся добавить книгу с пустым названием
        collector.add_new_book('')

        # проверяем, что книга не добавилась
        assert len(collector.get_books_genre()) == 0

    def test_add_new_book_with_too_long_name_does_not_add_book(self):
        # создаем экземпляр класса BooksCollector
        collector = BooksCollector()

        # пытаемся добавить книгу с названием длиннее 40 символов
        collector.add_new_book('А' * 41)

        # проверяем, что книга не добавилась
        assert len(collector.get_books_genre()) == 0

    # ---------- get_book_genre / set_book_genre ----------

    @pytest.mark.parametrize(
        'book_name, genre_to_set, expected_genre',
        [
            ('Шерлок Холмс', 'Детективы', 'Детективы'),
            ('1984', None, ''),
        ]
    )
    def test_get_book_genre_returns_expected_value(
        self, book_name, genre_to_set, expected_genre
    ):
        # создаем экземпляр класса BooksCollector
        collector = BooksCollector()

        # добавляем книгу
        collector.add_new_book(book_name)

        # если жанр задан — устанавливаем его
        if genre_to_set:
            collector.set_book_genre(book_name, genre_to_set)

        # проверяем, что метод возвращает ожидаемый жанр
        assert collector.get_book_genre(book_name) == expected_genre

    # ---------- get_books_with_specific_genre ----------

    def test_get_books_with_specific_genre_returns_only_books_with_given_genre(self):
        # создаем экземпляр класса BooksCollector
        collector = BooksCollector()

        # добавляем книги
        collector.add_new_book('Оно')
        collector.add_new_book('Сияние')
        collector.add_new_book('Дюна')

        # устанавливаем жанры
        collector.set_book_genre('Оно', 'Ужасы')
        collector.set_book_genre('Сияние', 'Ужасы')
        collector.set_book_genre('Дюна', 'Фантастика')

        # получаем список книг с жанром "Ужасы"
        result = collector.get_books_with_specific_genre('Ужасы')

        # проверяем, что вернулись только книги с нужным жанром
        assert sorted(result) == ['Оно', 'Сияние']

    # ---------- get_books_for_children ----------

    def test_get_books_for_children_excludes_books_with_age_rating_genres(self):
        # создаем экземпляр класса BooksCollector
        collector = BooksCollector()

        # добавляем книги
        collector.add_new_book('Король Лев')
        collector.add_new_book('Оно')

        # устанавливаем жанры
        collector.set_book_genre('Король Лев', 'Мультфильмы')
        collector.set_book_genre('Оно', 'Ужасы')

        # получаем список книг, подходящих для детей
        result = collector.get_books_for_children()

        # проверяем, что книга с возрастным рейтингом не попала в результат
        assert result == ['Король Лев']

    # ---------- get_books_genre ----------

    def test_get_books_genre_returns_current_dictionary(self):
        # создаем экземпляр класса BooksCollector
        collector = BooksCollector()

        # добавляем книги
        collector.add_new_book('Дюна')
        collector.add_new_book('1984')

        # формируем ожидаемый словарь вручную
        expected_books_genre = {
            'Дюна': '',
            '1984': ''
        }

        # проверяем, что метод возвращает словарь с актуальным состоянием books_genre
        assert collector.get_books_genre() == expected_books_genre

    # ---------- favorites ----------

    @pytest.mark.parametrize(
        'books',
        [
            ['Дюна'],
            ['Дюна', '1984'],
        ]
    )
    def test_get_list_of_favorites_books_returns_added_books(self, books):
        # создаем экземпляр класса BooksCollector
        collector = BooksCollector()

        # добавляем книги и добавляем их в избранное
        for book in books:
            collector.add_new_book(book)
            collector.add_book_in_favorites(book)

        # проверяем, что список избранного содержит добавленные книги
        assert collector.get_list_of_favorites_books() == books

    def test_add_book_in_favorites_does_not_add_duplicate(self):
        # создаем экземпляр класса BooksCollector
        collector = BooksCollector()

        # добавляем книгу
        collector.add_new_book('Дюна')

        # дважды добавляем книгу в избранное
        collector.add_book_in_favorites('Дюна')
        collector.add_book_in_favorites('Дюна')

        # проверяем, что книга в избранном только одна
        assert len(collector.get_list_of_favorites_books()) == 1

    def test_delete_book_from_favorites_removes_book(self):
        # создаем экземпляр класса BooksCollector
        collector = BooksCollector()

        # добавляем книгу и добавляем её в избранное
        collector.add_new_book('Дюна')
        collector.add_book_in_favorites('Дюна')

        # удаляем книгу из избранного
        collector.delete_book_from_favorites('Дюна')

        # проверяем, что список избранного пуст
        assert collector.get_list_of_favorites_books() == []
