# rehabstudio-gae-scaffold

![Docker](http://www.linux.com/news/galleries/image/docker?format=image&thumbnail=small)
![Appengine](http://bkarak.wizhut.com/blog/wp-content/uploads/2012/01/app_engine-64.png)
![Python](http://blog.magiksys.net/sites/default/files/pictures/python-logo-64.png)


***

**NOTE:** This scaffold is a fork of Google's [gae-secure-scaffold-python][gae-secure-scaffold-python] used under the terms of the Apache 2.0 license. Whilst we've tried to stay close to the original project, we've modified the layout extensively and made numerous updates (which are outlined in detail below).


## Introduction
***

This scaffold aims to make it as easy as possible to get started with Gogle Appengine, providing a secure application template including example handlers,
routes and tests. An example makefile is provided, containing sensible defaults
for management commands (running the development server, tests, deploying,
etc.).

This template uses [Docker][docker] to provide a standard development
environment for all developers on a project, this is the preferred method of
installation/development.


## Installing Docker
***

### Linux

Docker is best supported on Linux, you can probably find packages for your
preferred distribution [here][docker_install].

Once installed, skip ahead to [Getting the scaffold](#getting-the-scaffold) below.

### OSX

Installing and configuring Docker on OSX isn't quite as straightforward as it
is on Linux (yet). The [boot2docker][boot2docker] project provides a
lightweight Linux VM that acts as a (mostly) transparent way to run docker on
OSX.

First, install Docker and boot2docker following the instructions on
[this page][docker_osx_install]. Once you've installed Docker and launched
`boot2docker` for the first time, you need to stop it again so we can make
further modifications: `$ boot2docker stop`.

Since Docker on OSX is technically running inside a virtual machine and not
directly on the host OS, any volumes mounted will be on the VM's filesystem
and any bound ports will be exposed only to the boot2docker VM. We can work
around these limitations with a few tweaks to our setup.

In order to mount folders from your host OS into the boot2docker VM you'll
need to download a version of the boot2docker iso with Virtualbox's Guest
Additions installed:

    $ mkdir -p ~/.boot2docker
    $ curl http://static.dockerfiles.io/boot2docker-v1.2.0-virtualbox-guest-additions-v4.3.14.iso -o ~/.boot2docker/boot2docker.iso

Next, you need to tell Virtualbox to mount your `/Users` directory inside the
VM:

    $ VBoxManage sharedfolder add boot2docker-vm -name home -hostpath /Users

And that should be it. Let’s verify:

    $ boot2docker up
    $ boot2docker ssh "ls /Users"

You should see a list of all user's home folders from your host OS. Next, we
need to forward the appropriate ports so that we can reach the running
appengine development server directly from the host OS:

    $ VBoxManage controlvm boot2docker-vm natpf1 "aesdk,tcp,127.0.0.1,8080,,8080"
    $ VBoxManage controlvm boot2docker-vm natpf1 "aesdkadmin,tcp,127.0.0.1,8000,,8000"

And you should be ready to go, just follow the rest of the setup guide.

### Windows

![Tumbleweed](http://media.giphy.com/media/5x89XRx3sBZFC/giphy.gif)

No support yet (although it probably wouldn't take much). Pull requests very
welcome.


## Getting the scaffold
***

Whether you're running with Docker or have installed the Appengine SDK locally,
the first thing you'll need to do is get the code. This part is easy with
`git`:

    $ git clone https://github.com/rehabstudio/rehabstudio-gae-scaffold.git

Or without `git`:

    $ wget https://github.com/rehabstudio/rehabstudio-gae-scaffold/archive/master.zip
    $ unzip master.zip


## Using the scaffold
***

The easiest way to use this scaffold is with [Docker][docker]. With Docker
installed, running your application should be as simple as:

    $ make run

To run your application's tests, use the command:

    $ make test

Visit the running application [http://localhost:8080](http://localhost:8080)

Check out the `Makefile` in the repository root for all available commands.


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

See [LICENSE](LICENSE)


[boot2docker]: http://boot2docker.io/  "boot2docker"
[docker]: https://docker.io  "Docker"
[docker_install]: https://docs.docker.com/installation/  "Docker Installation"
[docker_osx_install]: https://docs.docker.com/installation/mac/  "Docker"
[gae-secure-scaffold-python]: https://github.com/google/gae-secure-scaffold-python
[thrdprty]: https://developers.google.com/appengine/docs/python/tools/libraries27  "Appengine third-party libraries"
