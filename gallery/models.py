# encoding: utf-8
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declared_attr

from flamaster.core.models import CRUDMixin
from flamaster.extensions import db

__all__ = ['FileModel', 'Album']


class GalleryMixin(CRUDMixin):
    """Base mixin for Gallery objects
    """
    name = db.Column(db.Unicode(512), nullable=False, default=u'')
    description = db.Column(db.UnicodeText, nullable=False, default=u'')
    is_public = db.Column(db.Boolean, default=True)

    @declared_attr
    def author_id(cls):
        return db.Column(
                db.Integer, db.ForeignKey("users.id"), nullable=False)

    @declared_attr
    def author(cls):
        return db.relationship('User',
                               backref=db.backref(cls.__tablename__,
                                                  lazy='dynamic'))

    def __repr__(self):
        return "<%s:%s>" % (self.__class__.__name__,
                            self.name)


class Album(db.Model, GalleryMixin):

    api_fields = ['id', 'name', 'description', 'coverage', 'total_images']

    def __init__(self, **kwargs):
        if 'owner' in kwargs:
            self.owner = kwargs.pop('owner')
        super(Album, self).__init__(**kwargs)

    @hybrid_property
    def coverage(self):
        image = self.images.filter_by(is_coverage=True)
        if image.count() == 0:
            image = self.images.order_by(func.random()).limit(1)

        image = image.first()
        return image and {'url': image.url, 'id': image.id} or None

    @coverage.setter
    def coverage(self, value):
        image = self.images.filter_by(id=value['id']).first()
        if image is not None:
            self.coverage and self.coverage.update(is_coverage=False)
            image.update(is_coverage=True)

    @property
    def public_images(self):
        return self.images.filter_by(is_public=True)

    # TODO: show all images to the owner and administrative roles
    @property
    def total_images(self):
        return self.public_images.count()

    def delete(self, commit=True):
        for image in self.images.all():
            image.delete()
        return super(Album, self).delete()

    @classmethod
    def create_defaults(cls, user):
        """ Ensure or create 2 albums for user with names 'default' and
            'userpic'
        """
        pass
        # if Album.query.filter_by(owner=kwargs['author_id']).count() == 0:
        #     Album.create(name='default', author_id=kwargs['author_id'])
        #     Album.create(name='userpic', author_id=kwargs['author_id'])

        # # TODO: understand how does it works with id of foreign object?
        # if 'album_id' not in kwargs:
        #     default_album = Album.query.filter_by(name='default').first().id
        #     kwargs['album_id'] = default_album


