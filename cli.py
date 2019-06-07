from mine import visualize_field, MineGameField


if __name__ == '__main__':
    def x_y_input():
        x = input("Enter x: ")
        y = input("Enter y: ")
        return (x, y)

    test_field = MineGameField(8, 8, n_of_bombs=4)
    visualize_field(test_field, hidden=False)
    print(3*'-\n')
    visualize_field(test_field)
    print(3*'-\n')
    while True:
        print("What do you want to do? (c, a, f): ")
        action = input("Enter (c, a, f): ")

        try:
            if action == 'c':
                x, y = x_y_input()
                cords = (int(x), int(y))
                test_field.player_check(cords)
            elif action == 'a':
                x, y = x_y_input()
                cords = (int(x), int(y))
                test_field.player_check_arround(cords)
            elif action == 'f':
                x, y = x_y_input()
                cords = (int(x), int(y))
                test_field.toggle_flag(cords)
            else:
                break
        except KeyError:
            print('Bad input. Try Again.')

        print(3*'-\n')
        visualize_field(test_field)
