# -*- coding: utf-8 -*-


@auth.requires_membership('ADM')
def index():

    list_str = """ 
        <tr class="odd gradeX">
            <td>%(nome)s</td>
            <td>%(papel)s</td>
            <td>
                <a href="%(edt)s" class="btn btn-primary btn-xs fa fa-pencil" ></a>
                <a href="%(delt)s" class="btn btn-primary btn-xs fa fa-trash-o" ></a>
            </td>

        </tr>
    """
    resp = db((db.auth_user.id == db.auth_membership.user_id) & (
        db.auth_group.id == db.auth_membership.group_id)).select()
    lista = [list_str % dict(nome=linha.auth_user.first_name,\
                             papel=linha.auth_group.role,\
                             edt=URL('papel', 'editar', args=linha.auth_membership.id),\
                             delt=URL('dispositivo', 'deletar', args=linha.auth_membership.id),\
                             )for linha in resp]
    return dict(lista=lista)


@auth.requires_membership('ADM')
def adicionar():
    form = SQLFORM(db.auth_membership, formstyle='divs')
    if form.process().accepted:
        response.flash = 'Sucesso!'
        redirect(URL('papel', 'index'))
    elif form.errors:
        response.flash = 'Erros!'
    else:
        response.flash = 'Preencha os dados'
    return dict(form=form)


@auth.requires_membership('ADM')
def editar():
    if request.args(0):
        record = db.auth_membership(request.args(0)) or redirect(URL('index'))
        form = SQLFORM(db.auth_membership, record, formstyle='divs')
    if form.process().accepted:
        redirect(URL('papel', 'index'))
        response.flash = 'Sucesso!'
    elif form.errors:
        response.flash = 'Erros!'
    else:
        response.flash = 'Preencha os dados'
    response.view = 'papel/adicionar.html'
    return dict(form=form)


@auth.requires_membership('ADM')
def deletar():
    try:
        if db(db.auth_membership.id == request.args(0)).delete():
            redirect(URL('papel', 'index'))
            response.flash = T('Registro Excluido com sucesso!')
        else:
            response.flash = T('Erro!')
    except Exception, e:
        response.flash = e
        pass
