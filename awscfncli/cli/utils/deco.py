import traceback
from functools import wraps

import botocore.exceptions
import click

from ...config import ConfigError


def boto3_exception_handler(f):
    """Capture and pretty print exceptions"""

    @wraps(f)
    def wrapper(ctx, *args, **kwargs):
        try:
            return f(ctx, *args, **kwargs)
        except (botocore.exceptions.ClientError,
                botocore.exceptions.WaiterError,
                botocore.exceptions.ValidationError,
                botocore.exceptions.ParamValidationError,
                ) as e:
            click.secho(str(e), fg='red')
            if ctx.obj.verbosity > 0:
                traceback.print_exc()
            raise click.Abort
        except ConfigError as e:
            click.secho(str(e), fg='red')
            if ctx.obj.verbosity > 0:
                traceback.print_exc()
            raise click.Abort

    return wrapper
