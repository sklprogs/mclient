from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message, rep

f = '[MClient] plugins.dsl.subjects.__main__'
    sh.com.start()
    timer = sh.Timer(f)
    timer.start()
    mes = Subjects().get_group('Wood processing')
    sh.objs.get_mes(f, mes, True).show_debug()
    timer.end()
    sh.com.end()

f = '[MClient] plugins.dsl.get.__main__'
    PATH = Home('mclient').add_config('dics')
    objs.get_all_dics().locate()

f = '[MClient] plugins.multitrandem.subjects.__main__'
    sh.com.start()
    timer = sh.Timer(f)
    timer.start()
    mes = Subjects().get_group('Wood processing')
    sh.objs.get_mes(f, mes, True).show_debug()
    timer.end()
    sh.com.end()

if __name__ == '__main__':
    f = '[MClient] plugins.multitrancom.utils.subjects.__main__'
    sh.com.start()
    mes = com.get_string(Loop().run())
    idebug = sh.Debug(f, mes)
    idebug.show()
    sh.com.end()


if __name__ == '__main__':
    f = '[MClient] plugins.stardict.subjects.__main__'
    sh.com.start()
    timer = sh.Timer(f)
    timer.start()
    mes = Subjects().get_group('Wood processing')
    sh.objs.get_mes(f, mes, True).show_debug()
    timer.end()
    sh.com.end()

if __name__ == '__main__':
    sh.com.start()
    model = TableModel()
    isave = Save()
    isave.set_model(model)
    isave.clear_selection()
    index_ = model.index(0, 0)
    isave.set_index(index_)
    isave.select_row(index_)
    # The font size is increased without changing the family in the controller
    isave.setFont(PyQt6.QtGui.QFont('Sans', 11))
    isave.show()
    sh.com.end()

if __name__ == '__main__':
    f = '[MClient] suggest.controller.Suggest.__main__'
    sh.com.start()
    lst = []
    for i in range(20):
        lst.append(f'item {i+1}')
    app = Suggest()
    app.fill(lst)
    app.go_end()
    app.show()
    app.set_width(96)
    mes = _('Goodbye!')
    sh.objs.get_mes(f, mes, True).show_debug()
    sh.com.end()

