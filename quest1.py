import sqlite3


class Location:
    def __init__(self, id):
        self.id = id
        self.pathes = self.get_unlock_pathes(id)

        s = ''.join(self.get_loc_text(id)[0])

        self.text = s

    def activate(self):
        path_texts = []
        return self.text, self.pathes

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

    def get_unlock_pathes(self, loc):
        con = sqlite3.connect(".\qests.db")
        cur = con.cursor()
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


class Path:
    def __init__(self, id, text, location, params):
        self.id = id
        self.text = text
        self.loc = location
        self.params = params

    def activate(self):
        if self.params != [None, None]:
            self.change_param(self.params[0], self.params[1])
        print(self.loc)
        return self.loc

    def change_param(self, change, param):
        con = sqlite3.connect(".\qests.db")
        cur = con.cursor()
        sqltxt = f"""UPDATE ParamsList
                        SET value = value {change}
                        WHERE paramID = {param}
"""
        cur.execute(sqltxt).fetchall()
        con.commit()
        con.close()


def read_quest(id):
    con = sqlite3.connect(".\qests.db")
    cur = con.cursor()
    sqltxt = f"""
    Select locID
    from start_locs
    Where start_locs.quest = "{id}"
    """
    result = cur.execute(sqltxt).fetchall()
    con.commit()
    con.close()
    return str(result[0][0])


def quests_list():
    con = sqlite3.connect(".\qests.db")
    cur = con.cursor()
    sqltxt = f"""
        Select quest, name
        from start_locs
        """
    result = cur.execute(sqltxt).fetchall()
    con.commit()
    con.close()
    return result


