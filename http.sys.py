#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# __author__ = 'hushpuppy'

import urllib2,sys,time
from burp import ITab
from burp import IBurpExtender
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator
from javax.swing import JLabel, JTextField, JOptionPane, JTabbedPane, JPanel, JButton
from java.awt import GridBagLayout, GridBagConstraints

class BurpExtender(IBurpExtender, IIntruderPayloadGeneratorFactory, ITab):
    name = "Http.sys fuzzing"
    args = ""
    binary = ""
    _jTabbedPane = JTabbedPane()
    _jPanel = JPanel()
    _jAboutPanel = JPanel()
    _jPanelConstraints = GridBagConstraints()
    _jLabelParameters = None
    _jTextFieldParameters = None
    _jLabelTechniques = None
    _jTextFieldTechniques = None
    _jLabelFuzzFactor = None
    _jTextFieldFuzzFactor = None
    _jLabelAdditionalCmdLine = None
    _jTextFieldAdditionalCmdLine = None
    _jButtonSetCommandLine = None
    _jLabelAbout = None
    aboutText = """
    <html><body><h1>made by hushpuppy</h1></body></html>
                    """

    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName(self.name)
        callbacks.registerIntruderPayloadGeneratorFactory(self)
        callbacks.addSuiteTab(self)
        self.initPanelConfig()
        self._jTabbedPane.addTab("Configuration", self._jPanel)
        self._jTabbedPane.addTab("About", self._jAboutPanel)
        return

    def getUiComponent(self):
        return self._jTabbedPane

    def getTabCaption(self):
        return "Http.sys fuzzing"

    def initPanelConfig(self):
        self._jPanel.setBounds(0, 0, 1000, 1000)
        self._jPanel.setLayout(GridBagLayout())

        self._jAboutPanel.setBounds(0, 0, 1000, 1000)
        self._jAboutPanel.setLayout(GridBagLayout())

        self._jLabelAdditionalCmdLine = JLabel("set url:")
        self._jPanelConstraints.fill = GridBagConstraints.HORIZONTAL
        self._jPanelConstraints.gridx = 0
        self._jPanelConstraints.gridy = 0
        self._jPanel.add(self._jLabelAdditionalCmdLine, self._jPanelConstraints)

        self._jTextFieldParameters = JTextField("",20)
        self._jPanelConstraints.fill = GridBagConstraints.HORIZONTAL
        self._jPanelConstraints.gridx = 1
        self._jPanelConstraints.gridy = 0
        self._jPanel.add(self._jTextFieldParameters, self._jPanelConstraints)

        self._jButtonSetCommandLine = JButton('go to test', actionPerformed=self.createNewInstance)
        self._jPanelConstraints.fill = GridBagConstraints.HORIZONTAL
        self._jPanelConstraints.gridx = 0
        self._jPanelConstraints.gridy = 5
        self._jPanelConstraints.gridwidth = 2
        self._jPanel.add(self._jButtonSetCommandLine, self._jPanelConstraints)

        self._jLabelAbout = JLabel("<html><body>%s</body></html>" % self.aboutText)
        self._jPanelConstraints.fill = GridBagConstraints.HORIZONTAL
        self._jPanelConstraints.gridx = 0
        self._jPanelConstraints.gridy = 0
        self._jAboutPanel.add(self._jLabelAbout, self._jPanelConstraints)
    def getGeneratorName(self):
        return "Http.sys fuzz"
    def createNewInstance(self,event=None):
        self.args = self._jTextFieldParameters.getText()
        print self.args
        if len(self.args) == 0:
            JOptionPane.showMessageDialog(None, "please input url")
        else:

            headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0",
                       "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                       "Accept-Language": "en-US,en;q=0.5",
                       "Accept-Encoding": "gzip, deflate",
                       "Range":"bytes=0-18446744073709551615",
                       "Host":"stuff"}
            try:
                t = urllib2.Request(self.args, headers=headers,timeout=5)
                r = urllib2.urlopen(t)
                JOptionPane.showMessageDialog(None, "working")
                if r.status_code == 416:

                    JOptionPane.showMessageDialog(None, "IIS Http.sys RCE")

                else:
                    JOptionPane.showMessageDialog(None, "don't have IIS Http.sys RCE")
                    # JOptionPane.showMessageDialog(None, "set over")
                # return r
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                JOptionPane.showMessageDialog(None, "time out or something wrong")
                return None

