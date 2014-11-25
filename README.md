# rehabstudio-gae-scaffold

![CircleCI Build Status](https://circleci.com/gh/rehabstudio/rehabstudio-gae-scaffold.svg?style=shield&circle-token=b2e58e2cb8e9e6e76e09ee39425a880830dc43a5)

***

**NOTE:** This scaffold is a fork of Google's
[gae-secure-scaffold-python][gae-secure-scaffold-python] used under the terms
of the Apache 2.0 license. Whilst we've tried to stay close to the original
project, we've modified the layout extensively and made numerous updates
(which are outlined in detail below).


## Introduction
***

This scaffold aims to make it as easy as possible to get started with Google
Appengine, providing a secure application template including example handlers,
routes and tests. An example makefile is provided, containing sensible defaults
for management commands (running the development server, tests, deploying,
etc.).

This template uses [Docker][docker] to provide a standard development
environment for all developers on a project, this is the preferred method of
installation/development.


## Security
***

The scaffold provides the following basic security guarantees by default through
a set of base classes found in `app/base/handlers.py`.  These handlers:

1. Set assorted security headers (Strict-Transport-Security, X-Frame-Options,
   X-XSS-Protection, X-Content-Type-Options, Content-Security-Policy) with
   strong default values to help avoid attacks like Cross-Site Scripting (XSS)
   and Cross-Site Script Inclusion.  See  `_SetCommonResponseHeaders()` and
   `SetAjaxResponseHeaders()`.
1. Prevent the XSS-prone construction of HTML via string concatenation by
   forcing the use of a template system (Jinja2 supported).  The
   template systems have non-contextual autoescaping enabled by default.
   See the `render()`, `render_json()` methods in `BaseHandler` and
   `BaseAjaxHandler`. For contextual autoescaping, you should use Closure
   Templates in strict mode (<https://developers.google.com/closure/templates/docs/security>).
1. Test for the presence of headers that guarantee requests to Cron or
   Task endpoints are made by the AppEngine serving environment or an
   application administrator.  See the `dispatch()` method in `BaseCronHandler`
   and `BaseTaskHandler`.
1. Verify XSRF tokens by default on authenticated requests using any verb other
   that GET, HEAD, or OPTIONS.  See the `_RequestContainsValidXsrfToken()`
   method for more information.

In addition to the protections above, the scaffold monkey patches assorted APIs
that use insecure or dangerous defaults (see `app/base/api_fixer.py`).

Obviously no framework is perfect, and the flexibility of Python offers many
ways for a motivated developer to circumvent the protections offered.  Under
the assumption that developers are not malicious, using the scaffold should
centralize many security mechanisms, provide safe defaults, and structure the
code in a way that facilitates security review.

Sample implementations can be found in `app/handlers.py`.  These demonstrate
basic functionality, and should be removed / replaced by code specific to
your application.


## Differences from gae-secure-scaffold-python
***

We've made some changes from the scaffold that Google provide. The major
changes are listed below, expect this list to grow over time as the scaffold
matures.

- Removed frontend-related code (to be re-added very soon).
- Added full docker setup to allow running in a consistent environment.
- Switched to a `make` based task runner for the overall application.
  - Original grunt and bash based build tools have been removed
  - A frontend build tool (grunt or gulp) will be used to manage frontend code
    but will be managed via the same makefile interface.
- Removed `src/` and `out/` directory.
  - Moved application code to `app/` directory.
  - Removed copy/build step for python code (javascript will still get built
    as required).
- Change how third-party code is used in the app.
  - Third-party (python) directory is now added to `sys.path` at runtime
    instead of copying to the application root.
- Enabled warmup requests in app.yaml.
- Removed support for Django templates, since we only use Jinja2.
- Tests run using nose and coverage with better test discovery.
- All tests and test related utils moved to a seperate folder.
- Routes can get messy, so now live in their own `routes.py` module for easier
  maintenance.
- PEP8 everywhere (sort of).


## Installing Docker
***

**NOTE:** The minimum required version of docker is 1.3. Docker/boot2docker
1.3.0 added support for mounted volumes when using boot2docker on OSX.

### Linux

Docker is best supported on Linux, you can probably find packages for your
preferred distribution [here][docker_install].

### OSX

Install Docker and boot2docker following the instructions on
[this page][docker_osx_install].

Next, we
need to forward the appropriate ports so that we can reach the running
appengine development server directly from the host OS:

    $ VBoxManage controlvm boot2docker-vm natpf1 "aesdk,tcp,127.0.0.1,8080,,8080"
    $ VBoxManage controlvm boot2docker-vm natpf1 "aesdkadmin,tcp,127.0.0.1,8000,,8000"

### Windows

Not supported yet (we just haven't tried, give it a go, it might work). Pull requests very welcome.


## Getting the scaffold
***

This part is easy with `git`:

    $ git clone https://github.com/rehabstudio/rehabstudio-gae-scaffold.git

You probably want to repoint the git remote `origin` to your own repository:

    $ git remote set-url origin git@github.com:me/my-repo.git


## Using the scaffold
***

With [Docker][docker] installed, running your application should be as simple
as:

    $ make run

Then visit the running application [http://localhost:8080](http://localhost:8080)

To run your application's tests, use the command:

    $ make test

To deploy your application to appengine, use:

    $ make deploy

If you wish to deploy to an application other than the default (defind in the
root-level Makefile) you can pass one of (or both) `app` or `version`
arguments to `make deploy` like so:

    $ make deploy app=someapp
    $ make deploy version=1
    $ make deploy app=someotherapp version=someotherversion

To open a bash shell inside the container environment, use:

    $ make shell

To run an IPython shell inside an appengine environment (with both your app
and all SDK modules importable), use:

    $ make pyshell

**Note:** When you want to run the python shell you must have already started
`make run` in another shell so we can access the remote API.

Check out the `Makefile` in the repository root for all available commands.


### Installing Libraries
***

See the [Third party libraries][thrdprty] page for libraries that are already
included in the SDK.  To include SDK libraries, add them in your `app.yaml`
file. Other than libraries included in the SDK, only pure python libraries may
be added to an App Engine project.

Any third-party Python modules added to the `app/third_party/py/` directory will be
added to Python's `sys.path` at runtime.


## Licensing
***

Apache 2.0. See [LICENSE](LICENSE)


[boot2docker]: http://boot2docker.io/  "boot2docker"
[docker]: https://docker.io  "Docker"
[docker_install]: https://docs.docker.com/installation/  "Docker Installation"
[docker_osx_install]: https://docs.docker.com/installation/mac/  "Docker"
[gae-secure-scaffold-python]: https://github.com/google/gae-secure-scaffold-python
[thrdprty]: https://developers.google.com/appengine/docs/python/tools/libraries27  "Appengine third-party libraries"
