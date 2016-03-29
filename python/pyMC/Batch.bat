@ECHO OFF
FOR /L %%A IN (1,1,8) DO (
  ECHO %%A
  ::start /B python dilutionExptMDRMDP.py -c %%A -f
  start /B python dilutionExptMDRMDP.py -c %%A
)