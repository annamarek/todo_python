-- models.sql
CREATE TABLE Users (
    id INT IDENTITY PRIMARY KEY,
    username NVARCHAR(50) UNIQUE NOT NULL,
    password_hash NVARCHAR(255) NOT NULL
);

CREATE TABLE Habits (
    id INT IDENTITY PRIMARY KEY,
    user_id INT FOREIGN KEY REFERENCES Users(id),
    name NVARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT GETDATE()
);

CREATE TABLE HabitLogs (
    id INT IDENTITY PRIMARY KEY,
    habit_id INT FOREIGN KEY REFERENCES Habits(id),
    log_date DATE NOT NULL,
    done BIT NOT NULL
);
