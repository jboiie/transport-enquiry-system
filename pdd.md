# 1. Product Description Document

Voice-Based Transport Enquiry System

## 1.1 Problem Statement

Accessing transport information like bus or train schedules often requires users to manually search through apps or websites, which can be slow, confusing, or inaccessible to some users. This becomes more difficult for elderly users, visually impaired users, or people who are not comfortable navigating digital interfaces.

There is a need for a simple system that allows users to query transport details using natural voice input and receive instant, accurate responses.

## 1.2 Proposed Solution

The Voice-Based Transport Enquiry System is an application that allows users to enquire about transport services such as buses and trains using voice commands. The system converts the spoken query into text, processes it, retrieves relevant data from a structured database, and responds with both on-screen text and voice output.

The database acts as the core of the system, storing transport schedules, routes, timings, and fares. Voice interaction is used only as an input and output interface, while all decision-making is handled through database queries.

## 1.3 Objectives

To design and implement a structured transport database

To enable voice-based querying of transport information

To retrieve accurate results using SQL queries

To provide user-friendly responses using text and speech

To demonstrate practical use of DBMS concepts in a real-world application

## 1.4 Scope of the Project

Supports enquiry for buses and trains

Allows queries based on source and destination

Displays transport type, timing, and fare

Works offline using a local database

Suitable for small-scale deployment

Future enhancements like live tracking or online APIs are out of scope for the current project.

## 1.5 Users of the System

General public

Elderly users

Visually impaired users

People with limited technical literacy

## 1.6 Functional Requirements

Accept voice input from the user

Convert voice input to text

Extract source, destination, and transport type

Query the database using SQL

Display results on screen

Read results aloud using text-to-speech

## 1.7 Non-Functional Requirements

Fast query response time

Simple and clean interface

Accurate speech recognition for basic commands

Reliable database storage