import bootstrap
from nark import *
from base import *
import base.webkit
import app
import os


@resolve(app.scope)
class App(object):

  def __init__(self, config=IConfig, session=ISession, db=IDb):

    self.config = config
    self.session = session
    self.db = db

    # Run database migrations, if any.
    self.upgrade_database()

    # Setup webkit
    a = self.session.assets
    files = a.base() + "/"
    path = a.resolve("index.html")
    self.webkit = base.webkit.Webkit(files, path)
    self.session.webkit = self.webkit

    # Attach views
    controller = Controller(self.webkit)
    controller.load(app.views)

    # Rebuild assets
    runner = Less()
    runner.watch(a.resolve("css"))

  def upgrade_database(self):
    """ Update the database using alembic, if it's installed.

        NB. To generate migration use: 
        alembic revision --autogenerate -m "Commit message"
    """
    try:
      run("alembic", "upgrade", "head")
    except BadCommandException:
      try:
        run("alembic.exe", "upgrade", "head")
      except BadCommandException:
        log.warn("Failed to update database: alembic is not installed and on the path")

  def run(self):
    """ Launch the UI """
    self.webkit.run()


log = Logging.get()
if __name__ == "__main__":
  app = App()
  app.run()
  os._exit(0)
