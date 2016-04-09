Feature: Sign Up
  As a system owner 
  I want new users to register with a username and password
  so that they can login to the system

  Scenario: Register New User
    Given a new user is at the signup page
    When the user enters a unique username and a password
    Then the user is registered and can login
