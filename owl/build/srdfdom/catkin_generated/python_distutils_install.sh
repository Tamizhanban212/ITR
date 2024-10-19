#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/tamizhanban/Documents/ITR/owl/src/srdfdom"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/tamizhanban/Documents/ITR/owl/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/tamizhanban/Documents/ITR/owl/install/lib/python3/dist-packages:/home/tamizhanban/Documents/ITR/owl/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/tamizhanban/Documents/ITR/owl/build" \
    "/usr/bin/python3" \
    "/home/tamizhanban/Documents/ITR/owl/src/srdfdom/setup.py" \
    egg_info --egg-base /home/tamizhanban/Documents/ITR/owl/build/srdfdom \
    build --build-base "/home/tamizhanban/Documents/ITR/owl/build/srdfdom" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/tamizhanban/Documents/ITR/owl/install" --install-scripts="/home/tamizhanban/Documents/ITR/owl/install/bin"
