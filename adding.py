from data.users import User
import data.db_session as db_session


db_session.global_init("db/blogs.db")
db_sess = db_session.create_session()

user = User()

user.surname = "Scott"
user.name = "Ridley"
user.age = 21
user.position = "captain"
user.speciality = "research engineer"
user.address = "module_1"
user.email = "scott_chief@mars.org"
user.hashed_password = "cap"

db_sess.add(user)

user = User()

user.surname = "Tom"
user.name = "Roling"
user.age = 19
user.position = "trainee"
user.speciality = "doctor"
user.address = "module_1"
user.email = "tom_rf@mars.org"
user.hashed_password = "doc"

db_sess.add(user)

user = User()

user.surname = "Ben"
user.name = "Jones"
user.age = 26
user.position = "middle"
user.speciality = "research engineer"
user.address = "module_2"
user.email = "jonesBen@mars.org"
user.hashed_password = "old"

db_sess.add(user)

user = User()

user.surname = "Matew"
user.name = "Benefresh"
user.age = 23
user.position = "trainee"
user.speciality = "research engineer"
user.address = "module_1"
user.email = "cooker_mat@mars.org"
user.hashed_password = "cooker"

db_sess.add(user)

db_sess.commit()