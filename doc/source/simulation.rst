.. _simulation:

Simulation
==========

* Multicompartmental model simulation


http://www.youtube.com/watch?v=Ikf6EU9kRG8&list=PL181D403527BD5A41&index=8&feature=plpp_video


* Biophysically realistic simulation of voltage across a neuronal morphology

  * Irregular 3D skeleton consisting of vertices and connectivity (segments)
  * Properties on the vertices and/or segments such as ion channel distributions etc.
  * Group of multiple trials with different initial condition and stimulation parameters

    * (Segment, time) array with voltage values across time.
    * (Stimulus, time) array representing the stimulus applied at specific timepoints, e.g. to segments

* Spiking network simulation with point neurons

Software writing HDF5:

* `neuroConstruct <http://www.neuroconstruct.org/>`_