class PageError():

    def __init__(self, error_id, error_name, error_description):
        self.error_id = error_id
        self.error_name = error_name
        self.error_description = error_description

# Пре создданые обьекты ошибки
error404 = PageError(404, "Страница не найдена", "К сожалению, запрошенная вами страница не существует или была перемещена. Возможно, вы ввели неверный адрес или страница была удалена.Если вы считаете, что это ошибка, пожалуйста, сообщите нам об этом на почту разработчика MONAHOVMM17@GMAIL.COM Мы постараемся устранить проблему как можно скорее.")