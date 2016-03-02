Spikey Appendix
===============

.. _label-clustersshkeygithub:

Setting up SSH keys on UHEI cluster for github.com
--------------------------------------------------

To create a key pair please follow the guide provided by github.com.
The configuration file for the ssh connection is located in ``~/.ssh/config``.
For example:

.. code-block:: bash

  $ cat .ssh/config
  Host github.com
      IdentityFile /wang/users/USERNAME/.ssh/my_github.com.id_rsa

The ``Host github.com`` describes the ``ssh`` connection target, and the following line
configures the private key location which will be used for this target host.

To connect via ssh, use the ``tsocks`` tool which routes the TCP connection via a local SOCKS proxy, e.g.:

.. code-block:: bash

  $ tsocks git clone git@github.com:USERNAME/PROJECT.git

