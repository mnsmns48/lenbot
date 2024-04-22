from datetime import datetime

from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates

from config import path, dobro_engine
from dobrotsen.tapp.crud import main_menu, walking_menu

pages_router = APIRouter()
templates = Jinja2Templates(directory="dobrotsen/tapp/templates")

current = datetime.now()
date = current.strftime("%d.%m.%Y")


@pages_router.get("/", response_model=None)
async def get_main(
        request: Request,
        session: AsyncSession = Depends(dobro_engine.session_dependency)
):
    data = await main_menu(session=session, parent=0)
    context = {'request': request, 'data': data.get('data')}
    return templates.TemplateResponse(
        name="menu.html",
        context=context
    )


@pages_router.get("/{parent}")
async def get_page_parent(
        parent: int,
        request: Request,
        session: AsyncSession = Depends(dobro_engine.session_dependency),

):
    data = await walking_menu(session=session, parent=parent)
    if data.get('end'):
        context = {"request": request, "data": data.get('data'), "parent": data.get('parent')}
        return templates.TemplateResponse(name="products.html", context=context)
    else:
        if data.get('data'):
            context = {"request": request, "data": data.get('data'), "parent": data.get('parent')}
            return templates.TemplateResponse(name="menu.html", context=context)
        else:
            context = {"request": request}
            return templates.TemplateResponse(name="none.html", context=context)