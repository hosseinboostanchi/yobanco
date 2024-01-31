/submit/expense/
  POST, returns a json
  input: date (optional), text, amount, token
  output: status:ok

/submit/income/
  POST, returns a json
  input: date (optional), text, amount, token
  output: result:ok

/accounts/login/
  POST, returns a json
  input: username, password
  output: status:ok & token



/q/generalstat/
  POST, returns a json
  input: fromdate (optional), todate(optional), token
  output: json from some general stats related to this user

/q/incomes/
  POST, returns json
  input: token, num (optional, default is 10)
  output: last num incomes

/q/expenses/
  POST, returns json
  input: token, num (optional, default is 10)
  output: last num  expenses