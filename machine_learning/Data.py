# loads the data and then converts it from csv to standard X, y array, assuming that we are dealing with R^2 to R^3 
def loading_data(data, index_X_data, index_Y_data_1): 
  with open(data) as csv_file:
      csv_reader = csv.reader(csv_file, delimiter=',')
      line_count = 0
      end_effector_store = []
      angles_store = []
      counter = 0
      for row in csv_reader:
        if row[index_X_data] is not None and row[index_X_data] != 'None' and counter > 0:
          # this converts the strings from the CSV to actual float tuples!
          floatTuple = tuple(float(ele) for ele in row[index_X_data].replace('(', '').replace(')', '').replace('...', '').split(', '))
          end_effector_store.append([floatTuple[0], floatTuple[1]])
          angles_store.append([float(row[index_Y_data_1]), float(row[index_Y_data_1+1]), float(row[index_Y_data_1+2])])
        counter += 1
      # print(end_effector_store)
      return end_effector_store, angles_store