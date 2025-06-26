# 🖥️ System Monitor

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![psutil](https://img.shields.io/badge/psutil-5.9.8-green)
![python-dotenv](https://img.shields.io/badge/python--dotenv-1.0.1-yellow)
![colorama](https://img.shields.io/badge/colorama-0.4.6-purple)
![License](https://img.shields.io/badge/License-MIT-orange)

</div>

A powerful system monitoring tool that provides real-time insights into your system's performance and sends detailed reports via email. Built with Python, this tool offers both interactive monitoring and automated email reporting capabilities.

## 🌟 Features

- **Real-time System Monitoring**
  - CPU Usage
  - Memory Usage
  - Battery Status
  - Network Usage
  - Storage Status
  - System Uptime

- **Email Reporting**
  - Automated system reports
  - Configurable sender and receiver
  - Secure credential management

- **Interactive Interface**
  - Color-coded output
  - Continuous monitoring mode
  - Customizable refresh intervals

## 🛠️ Tech Stack

- **Python 3.8+**: Core programming language
- **psutil**: System and process utilities
- **python-dotenv**: Environment variable management
- **colorama**: Cross-platform colored terminal text
- **smtplib**: Email functionality

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git
- Gmail account with App Password enabled

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone git@github.com:djdestinycodes/system-monitor.git
   cd system-monitor
   ```

2. **Create and activate virtual environment**
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure email settings**
   - Copy the example configuration file:
     ```bash
     cp example.config.txt config.txt
     ```
   - Edit `config.txt` with your email credentials:
     ```txt
     # Email Configuration
     SENDER_EMAIL=your-email@gmail.com
     EMAIL_PASSWORD=your-app-password
     RECEIVER_EMAIL=receiver-email@gmail.com
     ```

   > **Note**: 
   > - For Gmail, you need to use an App Password. [Learn how to generate one](https://support.google.com/accounts/answer/185833)
   > - The `example.config.txt` file serves as a template and includes detailed comments about each configuration option
   > - Never commit your `config.txt` file to version control

## 💻 Usage

### Basic System Information
```bash
python monitor.py
```

### Continuous Monitoring
```bash
python monitor.py --continuous
```

### Custom Refresh Interval
```bash
python monitor.py --continuous --interval 5.0
```

### Send Email Report
```bash
python monitor.py --email
```

## 🔒 Security

- Sensitive data is stored in `config.txt`
- The file is automatically ignored by git
- Never commit `config.txt` or `venv/` directory
- Use App Passwords for Gmail authentication
- `example.config.txt` is provided as a template and is safe to commit

## 📁 Project Structure

```
system-monitor/
├── monitor.py          # Main script
├── requirements.txt    # Project dependencies
├── example.config.txt  # Example configuration template
├── config.txt         # Email configuration (not tracked by git)
├── .gitignore        # Git ignore rules
└── venv/             # Virtual environment (not tracked by git)
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source, PLEASE HAVE FUN!!!

## 👨‍💻 Author

- **Dj Destiny** - [GitHub](https://github.com/djdestinycodes)

## 🙏 Acknowledgments

- [psutil](https://github.com/giampaolo/psutil) for system monitoring capabilities
- [python-dotenv](https://github.com/theskumar/python-dotenv) for environment management
- [colorama](https://github.com/tartley/colorama) for terminal coloring

---

<div align="center">
Made with ❤️ by Dj Destiny
</div> 