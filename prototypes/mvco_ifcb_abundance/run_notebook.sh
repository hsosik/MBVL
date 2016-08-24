#!/bin/bash
cd /vagrant
nohup ipython notebook --ip="*" &
nohup ipcluster start -n 4 &
