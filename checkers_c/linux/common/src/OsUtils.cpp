/*******************************************************************************
Copyright Intel Corporation.
This software and the related documents are Intel copyrighted materials, and
your use of them is governed by the express license under which they were
provided to you (License). Unless the License provides otherwise, you may not
use, modify, copy, publish, distribute, disclose or transmit this software or
the related documents without Intel's prior written permission. This software
and the related documents are provided as is, with no express or implied
warranties, other than those that are expressly stated in the License.

*******************************************************************************/

#include "OsUtils.h"

#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>

#include <array>
#include <sstream>

using std::endl;
using std::stringstream;

int OsUtils::RunCommand(const string cmd, string &out) {
  int exitStatus = 0;
  auto pPipe = popen(cmd.c_str(), "r");
  if (!pPipe) {
    return 1;
  }

  std::array<char, 256> buffer;
  while (fgets(buffer.data(), buffer.size(), pPipe) != nullptr) {
    out += buffer.data();
  }

  auto rc = pclose(pPipe);
  if (WIFEXITED(rc)) {
    exitStatus = WEXITSTATUS(rc);
  }

  return exitStatus;
}

OsType OsUtils::GetOsType() {
#if defined(WIN64) || defined(WIN32) || defined(WINIA64)
  return Windows;

#elif defined(MACI386) || defined(MACX86_64)
  return MacOs;

#elif defined(FREEBSD64)
  return FreeBSD;

#endif

  // #elif defined(LINX86) || defined(LINX64)
  string out;
  int exit_status;
  // Check that dpkg is installed
  exit_status = RunCommand("which dpkg 2>/dev/null", out);
  if (exit_status == 0) {
    return DebianBased;
  }

  // Check that rpm is installed
  exit_status = RunCommand("which rpm 2>/dev/null", out);
  if (exit_status == 0) {
    return RpmBased;
  }

  return UnknownOS;
}

passwd *OsUtils::GetPwUid(uid_t uid) { return getpwuid(uid); }

uid_t OsUtils::GetUid() { return getuid(); }

uid_t OsUtils::GetEUid() { return geteuid(); }

bool OsUtils::LoadFile(string path, string &message) {
  struct stat sb;
  int fd = open(path.c_str(), O_RDONLY);
  if (fstat(fd, &sb) == -1) { /* To obtain file size */
    stringstream ss;
    ss << "Cannot obtain length of file \"" << path << "\" " << endl;
    message = ss.str();
    return false;
  }

  const char *json =
      (const char *)mmap(nullptr, sb.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
  if (json == MAP_FAILED) {
    stringstream ss;
    ss << "Cannot read file \"" << path << "\" " << endl;
    message = ss.str();
    return false;
  }

  message = json;
  munmap((void *)json, sb.st_size);
  close(fd);
  return true;
}

int OsUtils::SetEnv(const char *name, const char *value, int replace) {
  return setenv(name, value, replace);
}

char *OsUtils::GetEnv(const char *name) { return getenv(name); }
