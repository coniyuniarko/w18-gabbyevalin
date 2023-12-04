
import datetime
from sqlalchemy import ScalarResult
from w18_gabbyevalin import db
from w18_gabbyevalin.model import Product


def product_list() -> ScalarResult[Product]:
    return db.session.execute(
        db.select(Product).order_by(Product.id)).scalars()


def product_by_id(id: int) -> Product:
    try:
        return db.session.execute(db.select(Product).filter_by(id=id)).scalar_one()
    except:
        return None


def product_create(title: str, description: str, priority: str, due_date: str) -> Product:
    try:
        product = Product(
            title=title,
            description=description,
            priority=priority,
            due_date=datetime.datetime.strptime(
                due_date, "%Y-%m-%d"),
        )
        db.session.add(product)
        db.session.commit()
        return product
    except:
        return None


def product_update(product: Product, title: str, description: str, priority: str, due_date: str) -> Product:
    try:
        product.title = title
        product.description = description
        product.priority = priority
        product.due_date = datetime.datetime.strptime(
            due_date, "%Y-%m-%d")
        db.session.commit()
        return product
    except:
        return None


def product_delete(product: Product) -> bool:
    try:
        db.session.delete(product)
        db.session.commit()
        return True
    except:
        print("Ada kesalahan dalam menyimpan produk baru")
    return False
