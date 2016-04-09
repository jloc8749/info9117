Feature: Login existing user
  As an existing user
  I want to login with a username and password
  so that I can access the users page

  Scenario: Login existing user
    Given an existing user is at the login page
    When the user enters a username and password which match a database entry
    Then the user is logged in and the users page is displayed
