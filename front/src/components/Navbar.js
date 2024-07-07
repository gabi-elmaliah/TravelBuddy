import React from 'react';
import { Component } from "react";
import "./NavbarStyles.css";
import { UnauthenticatedMenuItems, AuthenticatedMenuItems } from "./MenuItems";
import { Link } from "react-router-dom";

class Navbar extends Component
 {
  state = { clicked: false };

  handleClick = () => {
    this.setState({ clicked: !this.state.clicked });
  };

  handleLogout = () => {
    this.props.onLogout();
  };

  handleMenuItemClick = (item) => {
    if (item.title === "Logout") {
      this.handleLogout();
    }
  };

  render() {
    const { isAuthenticated } = this.props;
    const menuItems = isAuthenticated ? AuthenticatedMenuItems : UnauthenticatedMenuItems;

    return (
      <nav className="NavbarItems">
        <h1 className="Navbar-logo">Travel Buddy</h1>
        <div className="menu-icons" onClick={this.handleClick}>
          <i className={this.state.clicked ? "fas fa-times" : "fas fa-bars"}></i>
        </div>
        <ul className={this.state.clicked ? "nav-menu active" : "nav-menu"}>
          {menuItems.map((item, index) => (
            <li key={index}>
              <Link 
                className={item.cName} 
                to={item.url}
                onClick={() => this.handleMenuItemClick(item)}
              >
                <i className={item.icon}></i>
                {item.title}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    );
  }
}
export default Navbar;
