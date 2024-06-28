from database.crud.users import create_user_and_commit, read_users


def test_create_and_read_users(
        db_session,
        users,
):
    for item in users:
        create_user_and_commit(
            session=db_session,
            last_name=item["last_name"],
            first_name=item["first_name"],
            middle_name=item["middle_name"],
            hashed_password=item["hashed_password"],
        )

    result = read_users(session=db_session)
    assert len(result) == len(users)
    for index, item in enumerate(users):
        assert result[index].last_name == item["last_name"]
        assert result[index].first_name == item["first_name"]
        assert result[index].middle_name == item["middle_name"]
        assert result[index].hashed_password == item["hashed_password"]
