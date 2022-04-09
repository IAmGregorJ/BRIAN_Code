from passlib.hash import argon2

h = argon2.hash("password")
print(h)

j = argon2.using(rounds=4).hash("password")
print(j)

k = argon2.hash("password")
print(k)

print(argon2.verify("password", h))
print(argon2.verify("password", j))