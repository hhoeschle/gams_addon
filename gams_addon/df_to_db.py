__author__ = 'Hanspeter Hoeschle <hanspeter.hoeschle@gmail.com>'

import gams


def add_df_to_db(df, name, db, gams_type, result_type='L'):
    if gams_type == gams.GamsParameter:
        print "Add parameter from GamsDatabase"
        try:
            param = db.get_parameter(name)

            col_name = df.columns[0]
            if "Type" in df.index.names:
                index_cols = df.index.names
                df = df.reset_index()
                df = df[df["Type"] == result_type].set_index(index_cols)

                for idx in df.index:
                    gams_idx = [str(i) for i in idx[:-1]]
                    param.add_record(gams_idx).value = float(df.loc[idx, col_name])
            else:
                for idx in df.index:
                    gams_idx = [str(i) for i in idx]
                    param.add_record(gams_idx).value = float(df.loc[idx, col_name])

        except gams.GamsException as e:
            print e
            exit("Not yet implemented: Create new %s in db" % gams_type)

    else:
        exit("Not yet implemented: Add Symbol of type: %s" % gams_type)

    return db
