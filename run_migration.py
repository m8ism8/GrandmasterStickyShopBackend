import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from alembic.config import Config
from alembic import command

def run_migration():
    # Create Alembic configuration
    alembic_cfg = Config("alembic.ini")
    
    # Run the migration
    command.upgrade(alembic_cfg, "head")

if __name__ == "__main__":
    run_migration() 