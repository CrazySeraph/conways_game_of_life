import configparser

class MyApp:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    def read_config(self):
        name = self.config.get('General', 'name')
        age = self.config.getint('General', 'age')
        city = self.config.get('General', 'city')
        print(f"Name: {name}, Age: {age}, City: {city}")

    def update_config(self):
        self.config.set('General', 'name', 'Jane Doe')
        self.config.set('General', 'age', '25')
        self.config.set('General', 'city', 'London')

    def write_config(self):
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

# Create an instance of the MyApp class
app = MyApp()

# Read and display the configuration values
app.read_config()

# Update the configuration values
app.update_config()

# Write the updated configuration back to the file
app.write_config()
