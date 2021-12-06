def piece_retrieval_data(user_csv):
    print("Please select an activity or piece")

    previous_piece = []

    with open(user_csv, "r") as user_csv_file:
        user_csv_reader = csv.reader(user_csv_file)
        for line in user_csv_reader:
            if line[1] == "Activity":
                if line[3] not in previous_piece:
                    previous_piece.append(line[3])

    for index, piece in enumerate(previous_piece):
        print(f"[{index}] {piece}")

    try:
        piece_selection = int(input("Selection> "))
    except (TypeError, ValueError, IndexError):
        print("Please enter a valid number")

    # FIXME Error Handling
    user_piece = previous_piece[piece_selection]

    return user_piec