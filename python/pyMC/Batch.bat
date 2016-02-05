FOR /L %%A IN (1,1,12) DO (
  ECHO %%A
  start /B python logistic_model.py %%A
)