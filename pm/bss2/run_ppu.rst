Building and Running PPU Programs
=================================

.. _label-building_ppu:

Build PPU programs
------------------

To build programs for the PPU, the according file has to be mentioned in the *wscript* of the according repository.
Include the following code-snipped in the wscript to build a PPU program for HICANN-X.
To build a program for DLSv2 replace the *vx* with *v2*.

.. code-block:: python

  bld.program(
      features = 'cxx',
      target = 'name_of_ppu_program.bin',
      source = ['path_in_repo/name_of_ppu_program.cc'],
      use = ['nux_vx', 'nux_runtime_vx'],
      env = bld.all_envs['nux_vx'],
  )

To build the program follow the build step in :ref:`label-software_bss2`.
The according *.bin* file should be now in the */bin* folder for futher usage.


.. _label-running_ppu:

Run PPU programs
----------------

To run programs on the PPU there are specialiced functions for python.
To use them include the following in your experimental script.

**For HICANN-X**

.. code-block:: python

  from dlens_vx import halco
  from dlens_vx.tools.run_ppu_program import load_and_start_program, stop_program, wait_until_ppu_finished

  program_path = "bin/name_of_ppu_program.bin"
  ppu_id = 0  # Or 1 according which PPU should be used

  load_and_start_program(executor, program_path, ppu=halco.PPUOnDLS(ppu_id))
  wait_until_ppu_finished(executor, ppu=halco.PPUOnDLS(ppu_id))
  exit_code = stop_program(executor, ppu=halco.PPUOnDLS(ppu_id))

**For DLSv2**

.. code-block:: python

  from dlens_v2.tools.run_ppu_program import run_program

  program_path = "bin/name_of_ppu_program.bin"

  run_program(program_path)
