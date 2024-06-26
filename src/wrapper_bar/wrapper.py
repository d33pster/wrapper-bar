# MIT License

# Copyright (c) 2024 Soumyo Deep Gupta

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
wrapper module for wrapping commands across a progressbar.
"""

from io import TextIOWrapper
from os import getcwd as pwd
from os.path import join as jPath, abspath
from time import sleep
from datetime import datetime
from types import CodeType
import progressbar
import subprocess
import sys

from wrapper_bar.Exceptions import WrapperCodeDefinitionError

class Wrapper:
    """Wrapper Class: Wrap commands/scripts across a progress bar.
    
    `Usage:`
    >>> from wrapper_bar.wrapper import Wrapper
    
    >>> wrapControl = Wrapper()
    >>> wrapControl.decoy() # for demonstration.
    
    `Other Functions include:`
    >>> wrapControl.shellWrapper(<params>) # wrap shell commands into a progress bar.
    >>> wrapControl.pyWrapper(<params>) # wrap python scripts into a progress bar.
    >>> wrapControl.pyShellWrapper(<params>) # wrap inline python codes into a progress bar.
    
    `Parameters:`
    # Wrapper class
    >>> wrapControl = Wrapper(label:str (optional), marker:str (optional))
    # decoy function
    >>> wrapControl.decoy(delay:float (optional), width:float (optional))
    # shellWrapper function
    >>> wrapControl.shellWrapper(shellcommands:list[str], label:str = '' (optional),
                                 delay:float (optional),
                                 width:float (optional), timer:str (optional),
                                 logger:bool (optional), logfile:TextIOWrapper (optional),
                                 logfile_auto_close:bool (optional))
    # pyWrapper function
    >>> wrapControl.pyWrapper(pythonscripts:list[str], label:str = '' (optional),
                                delay:float (optional),
                                width:float (optional), timer:str (optional),
                                logger:bool (optional), logfile:TextIOWrapper (optional),
                                logfile_auto_close:bool (optional))
    # pyShellWrapper function
    >>> wrapControl.pyShellWrapper(pythoncodes: list[str], dependencies: list[str] (optional)
                                   label:str = '' (optional),
                                   timer:str = 'ETA' (optional), delay:float (optional),
                                   width:float (optional))
    
    # timer parameter
    default: 'ETA'
    possible values: ['ETA', 'ElapsedTime']
    
    # pyShellWrapper parameters
    pythoncodes -> list of python codes
    dependencies -> list of dependencies. Suppose 'a = b+c' is among the python codes list.
                    Therefore, b and c's value are dependencies and depencies=['b=10', 'c=115'].

    NOTE: Avoid using any print, return or yield statements to avoid breaking the progress bar.
    
    # How to get the value of 'a' from 'a=b+c' after execution?
    >>> a = wrapControl.pyShellWrapperResults['a']
    
    For Beginners, wrapping commands across a given progress bar might seem
    awfully time consuming. This Module is an effort to provide satisfaction to
    your aesthetic needs for your scripts.
    
    Feel free to check out the code and do any modifications you like under the
    MIT License. ;)
    """
    def __init__(self, marker:str = "▓") -> None:
        """Initialize the Wrapper class"""
        self.marker = marker
    
    def decoy(self, label:str = "", delay: float = 0.1, width:float = 50, timer: str = 'ETA'):
        """Create a decoy progress bar, that does nothing at all.
        
        `steps`:
        >>> wrapControl = Wrapper()
        >>> wrapControl.decoy()
        """
        if timer=='ETA':
            widgets = [label+" ", progressbar.Bar(marker=self.marker), progressbar.AdaptiveETA()]
        elif timer=='ElapsedTime':
            widgets = [label+" ", progressbar.Bar(marker=self.marker), progressbar.Timer()]
        else:
            widgets = [label+" ", progressbar.Bar(marker=self.marker), progressbar.AdaptiveETA()]
            
        try:
            bar = progressbar.ProgressBar(widgets=widgets, maxval=100, term_width=width).start()
            
            for i in range(100):
                sleep(delay)
                bar.update(i)
            
            bar.finish()
        except KeyboardInterrupt:
            pass
    
    def shellWrapper(self, shellcommands: list[str], label:str = "", delay: float = 0.1, width:float = 50, timer: str = 'ETA',
                     logger:bool = False, logfile:TextIOWrapper = None, logfile_auto_close:bool = False):
        """Wrap shell commands with the progressbar.
        
        `steps`:
        >>> wrapControl.shellWrapper(shellcommands:list[str], label:str = '' (optional),
                                    delay:float (optional),
                                    width:float (optional), timer:str (optional),
                                    logger:bool (optional), logfile:TextIOWrapper (optional),
                                    logfile_auto_close:bool (optional))

        `timer` parameter:
        default: 'ETA'
        possible values: ['ETA', 'ElapsedTime']
        """
        if logger:
            if not logfile:
                logfile = open(jPath(pwd(), '.log'), 'w')
        
        if timer=='ETA':
            widgets = [label+" ", progressbar.Bar(marker=self.marker), progressbar.AdaptiveETA()]
        elif timer=='ElapsedTime':
            widgets = [label+" ", progressbar.Bar(marker=self.marker), progressbar.Timer()]
        else:
            widgets = [label+" ", progressbar.Bar(marker=self.marker), progressbar.AdaptiveETA()]
        
        try:
            bar = progressbar.ProgressBar(widgets=widgets, term_width=width, maxval=100).start()
            
            interval = int(100/(len(shellcommands)+1))
            iterator = 0
            
            for i in range(100):
                if i>=interval and (i==interval or i%interval==0) and iterator<len(shellcommands):
                    logfile.write(f"{datetime.today().strftime('%B %d, %Y')} {datetime.now().strftime('%H hours %M minutes %S seconds')}\n")
                    logfile.write(f"Command Executed: \'{shellcommands[iterator]}\'\n")
                    subprocess.Popen(shellcommands[iterator].split(' '), stderr=logfile, stdout=logfile).wait()
                    logfile.write(f'\nEND\n')
                    iterator += 1
                    bar.update(i)
                else:
                    sleep(delay)
                    bar.update(i)
            
            bar.finish()
        except KeyboardInterrupt:
            pass
        
        if logfile_auto_close:
            logfile.close()
    
    def pyWrapper(self, pythonscripts: list[str], label:str = "", delay: float = 0.1, width: float = 50, timer:str = 'ETA',
                  logger:bool = False, logfile: TextIOWrapper = None, logfile_auto_close:bool = False):
        """Wrap Python Scripts with the progressbar.
        
        `steps`:
        >>> wrapControl.pyWrapper(pythonscripts:list[str], label:str = '' (optional),
                                delay:float (optional),
                                width:float (optional), timer:str (optional),
                                logger:bool (optional), logfile:TextIOWrapper (optional),
                                logfile_auto_close:bool (optional))
        
        `timer` parameter:
        default: 'ETA'
        possible values: ['ETA', 'ElapsedTime']
        """
        if logger:
            if not logfile:
                logfile = open(jPath(pwd(), '.log'), 'w')
        
        for i in range(len(pythonscripts)):
            pythonscripts[i] = abspath(pythonscripts[i])
        
        if timer=='ETA':
            widgets = [label+" ", progressbar.Bar(marker=self.marker), progressbar.AdaptiveETA()]
        elif timer=='ElapsedTime':
            widgets = [label+" ", progressbar.Bar(marker=self.marker), progressbar.Timer()]
        else:
            widgets = [label+" ", progressbar.Bar(marker=self.marker), progressbar.AdaptiveETA()]
        
        try:
            bar = progressbar.ProgressBar(widgets=widgets, maxval=100, term_width=width).start()
            
            interval = int(100/(len(pythonscripts)+1))
            iterator = 0
            
            for i in range(100):
                if i>=interval and (i==interval or i%interval==0) and iterator<len(pythonscripts):
                    logfile.write(f"{datetime.today().strftime('%B %d, %Y')} {datetime.now().strftime('%H hours %M minutes %S seconds')}\n")
                    logfile.write(f"Python File Executed: \'{pythonscripts[iterator]}\'\n")
                    subprocess.Popen(['python'].extend(pythonscripts[iterator].split(' ')), stderr=logfile).wait()
                    logfile.write(f"\nEND\n")
                    iterator += 1
                    bar.update(i)
                else:
                    sleep(delay)
                    bar.update(i)
            
            bar.finish()
        except KeyboardInterrupt:
            pass
        
        if logfile_auto_close:
            logfile.close()
    
    def __compile(self, codes:list[str]) -> list[CodeType]:
        compiledcodes:list[CodeType] = []
        for code in codes:
            compiledcode = compile(code, '<string>', 'exec')
            compiledcodes.append(compiledcode)
        
        return compiledcodes
    
    def pyShellWrapper(self, pythoncodes: list[str], dependencies:list[str] = [], label:str = "", delay:float = 0.1, width:float = 50,
                       timer:str = 'ETA'):
        """Wrap inline python codes with a progressbar
        
        `steps`:
        >>> wrapControl.pyShellWrapper(pythoncodes: list[str], dependencies: list[str] (optional)
                                   label:str = '' (optional),
                                   timer:str = 'ETA' (optional), delay:float (optional),
                                   width:float (optional))
    
        `timer` parameter:
        default: 'ETA'
        possible values: ['ETA', 'ElapsedTime']
        
        `pyShellWrapper` parameters:
        pythoncodes -> list of python codes
        dependencies -> list of dependencies. Suppose 'a = b+c' is among the python codes list.
                        Therefore, b and c's value are dependencies and depencies=['b=10', 'c=115'].
        """
        
        codes = []
        self.__pyshellresults = {}
        
        variables=""""""
        for c in dependencies:
            variables += c + "\n"
        
        for x in pythoncodes:
            code = variables + x + "\n"
            codes.append(code)
        
        try:
            compiledcodes = self.__compile(codes=codes)
        except KeyboardInterrupt:
            sys.exit(1)

        
        if timer=='ETA':
            widgets = [label+" ", progressbar.Bar(marker=self.marker), progressbar.AdaptiveETA()]
        elif timer=='ElapsedTime':
            widgets = [label+" ", progressbar.Bar(marker=self.marker), progressbar.Timer()]
        else:
            widgets = [label+" ", progressbar.Bar(marker=self.marker), progressbar.AdaptiveETA()]
        
        try:
            bar = progressbar.ProgressBar(widgets=widgets, maxval=100, term_width=width).start()
            
            interval = int(100/(len(pythoncodes)+1))
            iterator = 0
            
            for i in range(100):
                if i>=interval and (i==interval or i%interval==0) and iterator<len(pythoncodes):
                    exec(compiledcodes[iterator], globals(), self.__pyshellresults)
                    iterator += 1
                    bar.update(i)
                else:
                    sleep(delay)
                    bar.update(i)
            
            bar.finish()
        except KeyboardInterrupt:
            pass
    
    def __fetchPyShellWrapperResults(self):
        return self.__pyshellresults
    
    pyShellWrapperResults = property(fget=__fetchPyShellWrapperResults)