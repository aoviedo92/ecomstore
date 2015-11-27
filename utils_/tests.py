# class A:
#     def __init__(self):
#         self.__a = 10
#
#     @property
#     def a(self):
#         return self.__a
#
#     @a.setter
#     def a(self, value):
#         self.__a = value
#
#     def sum(self):
#         return [self.__a, 1, 2, 3]
#
#
# class B(object, A):
#     def __init__(self):
#         A.__init__(self)
#         # super(B, self).__init__()
#         self.a = 40
#
#
# print B().sum()[:3]
