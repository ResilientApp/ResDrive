import React, {useRef, useState} from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Input, Image, Button, message } from "antd";
import './Drive.css';
import usernameLogo from "./resource/username_logo.png";
import lockLogo from "./resource/lock_logo.png";
import resdbLogo from "./resource/resilientdb_logo.svg";
import ucdavisLogo from "./resource/ucdavis_logo.png";
import githubLogo from "./resource/github_logo.svg";
import reschatLogo from "./resource/reschat_logo.svg"

function Drive() {
    return (
        <div className={'webPage'}>
            <div className={'driveBox'}></div>
        </div>
    );
}



export default Drive;