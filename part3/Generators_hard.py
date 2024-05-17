import types
from datetime import datetime
from itertools import chain

"""
Необязательное задание. Написать генератор, аналогичный генератору из задания 2, но обрабатывающий списки с любым 
уровнем вложенности. Шаблон и тест в коде ниже:
"""


def decorator_with_params(path):
    def decorator(old_function):
        def new_function(*args, **kwargs):
            with open(path, 'w', encoding='utf-8') as f:
                f.write(f'Time: {datetime.now()}\n')
                f.write(f'Function name: {old_function.__name__}\n')
                f.write(f'params {args=} and {kwargs}\n')
                result = old_function(*args, **kwargs)
                f.write(f'{result=}')

            return result

        return new_function

    return decorator


def test_3():
    paths = ('part3/dec1.log', 'part3/dec2.log', 'part3/dec3.log')

    for path in paths:

        @decorator_with_params(path)
        def flat_generator(list_of_list):
            for i in list_of_list:
                if isinstance(i, list):
                    for j in flat_generator(i):
                        yield j
                else:
                    yield i

        list_of_lists_2 = [
            [['a'], ['b', 'c']],
            ['d', 'e', [['f'], 'h'], False],
            [1, 2, None, [[[[['!']]]]], []]
        ]

        for flat_iterator_item, check_item in zip(
                flat_generator(list_of_lists_2),
                ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
        ):
            assert flat_iterator_item == check_item

        assert list(flat_generator(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']

        assert isinstance(flat_generator(list_of_lists_2), types.GeneratorType)
