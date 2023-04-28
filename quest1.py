import sqlite3


# класс локации


class Location:
    '''
    класс для создания обьекта локации
    чтобы создать локацию, в него нужно передать только ID локации из базы данных.
    класс создан для взаимодейсьвия с классом Path
    функции этого класса вернут все необходимые данные для создания обьекта пути
    '''

    def __init__(self, id):
        self.id = id

        # получение всех путей из этой локации
        self.pathes = self.get_unlock_pathes(id)

        # Получение текста локации
        s = ''.join(self.get_loc_text(id)[0])
        self.text = s

    def activate(self):
        path_texts = []
        return self.text, self.pathes

    # функция возвращает текст локации с определенным номером

    def get_loc_text(self, loc):
        con = sqlite3.connect(".\qests.db")
        cur = con.cursor()
        sqltxt = f"""
            Select TxtLoc
            from Loc
            Where Loc.LocID = "{loc}"
            """
        result = cur.execute(sqltxt).fetchall()
        con.commit()
        con.close()
        print(result)
        return result

    # функция возвращает все доступные пути из локации
    def get_unlock_pathes(self, loc):
        # подключение к базе
        con = sqlite3.connect(".\qests.db")
        cur = con.cursor()

        # запрос в базу данных на получение доступных путей
        sqltxt = f"""
    Select Loc_to_Path.Path, Pathes.text, Pathes.LocTarget, Params.Change, ParamsList.ParamID, ParamsList.value
    from Loc_to_Path
       INNER JOIN Pathes
            ON Pathes.pathid = Loc_to_Path.Path
        Left JOIN Params
            ON Pathes.pathid = Params.Path
        Left JOIN ParamsList
            ON ParamsList.ParamID = Params.ParamID
     Where Loc_to_Path.LocId = '{loc}' and (ParamsList.value >= Params.Req or Params.Req is NULL)
    """
        result = cur.execute(sqltxt).fetchall()
        con.commit()
        con.close()
        return result


# класс для создания пути
class Path:
    '''
    класс для создания обьекта локации
    чтобы создать локацию, в него нужно передать:
     ID пути, его текст, целевую локацию и изменяемые параметры из базы данных.
    класс создан для взаимодейсьвия с классом Location
    функции этого класса вернут все необходимые данные для создания обьекта локации
    '''

    def __init__(self, id, text, location, params):
        self.id = id
        self.text = text
        self.loc = location
        self.params = params

    # функция, возвращающая локацию
    def activate(self):
        if self.params != [None, None]:
            self.change_param(self.params[0], self.params[1])
        print(self.loc)
        return self.loc

    def change_param(self, change, param):
        # подключение к базе
        con = sqlite3.connect(".\qests.db")
        cur = con.cursor()

        # запрос в базу данных на
        sqltxt = f"""UPDATE ParamsList
                        SET value = value {change}
                        WHERE paramID = {param}
"""
        cur.execute(sqltxt).fetchall()
        con.commit()
        con.close()


# функция возвращает
def read_quest(id):
    # подключение к базе
    con = sqlite3.connect(".\qests.db")
    cur = con.cursor()

    # запрос в базу данных на получение стартовой локации
    sqltxt = f"""
    Select locID
    from start_locs
    Where start_locs.quest = "{id}"
    """
    result = cur.execute(sqltxt).fetchall()
    con.commit()
    con.close()

    # возврат номера стартовой локации
    return str(result[0][0])


def quests_list():
    # подключение к базе
    con = sqlite3.connect(".\qests.db")
    cur = con.cursor()

    # запрос в базу данных на получение списка квестов
    sqltxt = f"""
        Select quest, name
        from start_locs
        """
    result = cur.execute(sqltxt).fetchall()
    con.commit()
    con.close()
    return result


