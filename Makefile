NAME = opengl_app
CXX = g++
CC = gcc
CXXFLAGS = -g -Wall -Wextra -std=c++17
CFLAGS = -g -Wall -Wextra
INCS = -I./glad/include
LIBS = -lglfw -lGL -lX11 -lpthread -lXrandr -lXi -ldl -lm
CPP_SRCS = hello_world.cpp
C_SRCS = glad/src/glad.c

OBJS = $(CPP_SRCS:.cpp=.o) $(C_SRCS:.c=.o)

all: $(NAME)

$(NAME): $(OBJS)
	$(CXX) $(OBJS) -o $(NAME) $(LIBS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(INCS) -c $< -o $@

%.o: %.c
	$(CC) $(CFLAGS) $(INCS) -c $< -o $@

clean:
	rm -f $(OBJS)

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re