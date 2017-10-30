#!/usr/bin/python
"""

Original script based upon:

Copyright (c) 2017 Intel Corporation All Rights Reserved.

THESE MATERIALS ARE PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL INTEL OR ITS
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THESE
MATERIALS, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

File Name: sys_analyzer-s.py

Abstract: Script for checking the environment for Intel Media Server Studio
Media SDK and SDK for OpenCL Applications install and run readiness

Notes: Run sys_analyzer-s.py
Notes: THIS SCRIPT IS MODIFIED TO IDENTIFY CPU and GPU
Notes: small version

"""

import os, sys, platform
import os.path

class diagnostic_colors:
    ERROR   = '\x1b[31;1m'  # Red/bold
    SUCCESS = '\x1b[32;1m'  # green/bold
    RESET   = '\x1b[0m'     # Reset attributes
    INFO    = '\x1b[34;1m'  # info
    OUTPUT  = ''            # command's coutput printing
    STDERR  = '\x1b[36;1m'  # cyan/bold
    SKIPPED = '\x1b[33;1m'  # yellow/bold

class loglevelcode:
    ERROR   = 0
    SUCCESS = 1
    INFO    = 2

GLOBAL_LOGLEVEL=1

def print_info( msg, loglevel ):
    global GLOBAL_LOGLEVEL

    """ printing information """    
    
    if loglevel==loglevelcode.ERROR and GLOBAL_LOGLEVEL>=0:
        color = diagnostic_colors.ERROR
        msgtype=" [ ERROR ] "
        print( color + msgtype + diagnostic_colors.RESET + msg )
    elif loglevel==loglevelcode.SUCCESS and GLOBAL_LOGLEVEL>=1:
        color = diagnostic_colors.SUCCESS
        msgtype=" [ OK ] "
        print( color + msgtype + diagnostic_colors.RESET + msg )
    elif loglevel==loglevelcode.INFO and GLOBAL_LOGLEVEL>=2:
        color = diagnostic_colors.INFO
        msgtype=" [ INFO ] "
        print( color + msgtype + diagnostic_colors.RESET + msg )


    
    return

def run_cmd(cmd):
    output=""
    fin=os.popen(cmd+" 2>&1","r")
    for line in fin:
        output+=line
    fin.close()
    return output

def find_library(libfile):
    search_path=os.environ.get("LD_LIBRARY_PATH","/usr/lib64")
    if not ('/usr/lib64' in search_path):
	search_path+=";/usr/lib64"
    paths=search_path.split(";")

    found=False
    for libpath in paths:
        if os.path.exists(libpath+"/"+libfile):
            found=True
            break
    
    return found


def parse_pciid(pciid):
    sts=loglevelcode.ERROR
    gpustr="unknown"

    id_directory={
    '0402':'HSW GT1 desktop',
    '0412':'HSW GT2 desktop',
    '0422':'HSW GT3 desktop',
    '040a':'HSW GT1 server',
    '041a':'HSW GT2 server',
    '042a':'HSW GT3 server',
    '040B':'HSW GT1 reserved',
    '041B':'HSW GT2 reserved',
    '042B':'HSW GT3 reserved',
    '040E':'HSW GT1 reserved',
    '041E':'HSW GT2 reserved',
    '042E':'HSW GT3 reserved',
    '0C02':'HSW SDV GT1 desktop',
    '0C12':'HSW SDV GT2 desktop',
    '0C22':'HSW SDV GT3 desktop',
    '0C0A':'HSW SDV GT1 server',
    '0C1A':'HSW SDV GT2 server',
    '0C2A':'HSW SDV GT3 server',
    '0C0B':'HSW SDV GT1 reserved',
    '0C1B':'HSW SDV GT2 reserved',
    '0C2B':'HSW SDV GT3 reserved',
    '0C0E':'HSW SDV GT1 reserved',
    '0C1E':'HSW SDV GT2 reserved',
    '0C2E':'HSW SDV GT3 reserved',
    '0A02':'HSW ULT GT1 desktop',
    '0A12':'HSW ULT GT2 desktop',
    '0A22':'HSW ULT GT3 desktop',
    '0A0A':'HSW ULT GT1 server',
    '0A1A':'HSW ULT GT2 server',
    '0A2A':'HSW ULT GT3 server',
    '0A0B':'HSW ULT GT1 reserved',
    '0A1B':'HSW ULT GT2 reserved',
    '0A2B':'HSW ULT GT3 reserved',
    '0D02':'HSW CRW GT1 desktop',
    '0D12':'HSW CRW GT2 desktop',
    '0D22':'HSW CRW GT3 desktop',
    '0D0A':'HSW CRW GT1 server',
    '0D1A':'HSW CRW GT2 server',
    '0D2A':'HSW CRW GT3 server',
    '0D0B':'HSW CRW GT1 reserved',
    '0D1B':'HSW CRW GT2 reserved',
    '0D2B':'HSW CRW GT3 reserved',
    '0D0E':'HSW CRW GT1 reserved',
    '0D1E':'HSW CRW GT2 reserved',
    '0D2E':'HSW CRW GT3 reserved',
    '0406':'HSW GT1 mobile',
    '0416':'HSW GT2 mobile',
    '0426':'HSW GT2 mobile',
    '0C06':'HSW SDV GT1 mobile',
    '0C16':'HSW SDV GT2 mobile',
    '0C26':'HSW SDV GT3 mobile',
    '0A06':'HSW ULT GT1 mobile',
    '0A16':'HSW ULT GT2 mobile',
    '0A26':'HSW ULT GT3 mobile',
    '0A0E':'HSW ULX GT1 mobile',
    '0A1E':'HSW ULX GT2 mobile',
    '0A2E':'HSW ULT GT3 reserved',
    '0D06':'HSW CRW GT1 mobile',
    '0D16':'HSW CRW GT2 mobile',
    '0D26':'HSW CRW GT3 mobile',
    '1602':'BDW GT1 ULT',
    '1606':'BDW GT1 ULT',
    '160B':'BDW GT1 Iris',
    '160E':'BDW GT1 ULX',
    '1612':'BDW GT2 Halo',
    '1616':'BDW GT2 ULT',
    '161B':'BDW GT2 ULT',
    '161E':'BDW GT2 ULX',
    '160A':'BDW GT1 Server',
    '160D':'BDW GT1 Workstation',
    '161A':'BDW GT2 Server',
    '161D':'BDW GT2 Workstation',
    '1622':'BDW GT3 ULT',
    '1626':'BDW GT3 ULT',
    '162B':'BDW GT3 Iris',
    '162E':'BDW GT3 ULX',
    '162A':'BDW GT3 Server',
    '162D':'BDW GT3 Workstation',
    '1632':'BDW RSVD ULT',
    '1636':'BDW RSVD ULT',
    '163B':'BDW RSVD Iris',
    '163E':'BDW RSVD ULX',
    '163A':'BDW RSVD Server',
    '163D':'BDW RSVD Workstation',
    '1906':'SKL ULT GT1',
    '190E':'SKL ULX GT1',
    '1902':'SKL DT GT1',
    '190B':'SKL Halo GT1',
    '190A':'SKL SRV GT1',
    '1916':'SKL ULT GT2',
    '1921':'SKL ULT GT2F',
    '191E':'SKL ULX GT2',
    '1912':'SKL DT GT2',
    '191B':'SKL Halo GT2',
    '191A':'SKL SRV GT2',
    '191D':'SKL WKS GT2',
    '1923':'SKL ULT GT3',
    '1926':'SKL ULT GT3',
    '1927':'SKL ULT GT3',
    '192B':'SKL Halo GT3',
    '192D':'SKL SRV GT3',
    '1932':'SKL DT GT4',
    '193B':'SKL Halo GT4',
    '193D':'SKL WKS GT4',
    '192A':'SKL SRV GT4',
    '193A':'SKL SRV GT4e',
    '5A84':'APL HD Graphics 505',
    '5A85':'APL HD Graphics 500',
    '5913':'KBL ULT GT1.5',
    '5915':'KBL ULX GT1.5',
    '5917':'KBL DT GT1.5',
    '5906':'KBL ULT GT1',
    '590E':'KBL ULX GT1',
    '5902':'KBL DT GT1',
    '5908':'KBL Halo GT1',
    '590B':'KBL Halo GT1',
    '590A':'KBL SRV GT1',
    '5916':'KBL ULT GT2',
    '5921':'KBL ULT GT2F',
    '591E':'KBL ULX GT2',
    '5912':'KBL DT GT2',
    '591B':'KBL Halo GT2',
    '591A':'KBL SRV GT2',
    '591D':'KBL WKS GT2',
    '5923':'KBL ULT GT3',
    '5926':'KBL ULT GT3',
    '5927':'KBL ULT GT3',
    '593B':'KBL Halo GT4'}


    try:
        gpustr=id_directory[pciid]
        sts=loglevelcode.SUCCESS
    except:
        pass

    return (sts,gpustr)

def get_processor():
    processor_name="unknown"
    f=open("/proc/cpuinfo","r")
    for line in f:
        if line.find("model name")<0: continue
        line=line.strip()
        (var,val)=line.split(":")
        processor_name=val
        break

    return processor_name.strip()



def does_processor_have_gen_graphics():
    processor_name=get_processor()
    print_info("Processor name: "+processor_name,loglevelcode.SUCCESS)
    processor_name=processor_name.upper()	


    if (processor_name.find("INTEL")>=0):
        print_info("Intel Processor",loglevelcode.INFO) 
    else:
        print_info("Not an Intel processor.  No Media GPU capabilities supported.",loglevelcode.ERROR)


    if (processor_name.find("CORE")>=0):
        print_info("Processor brand: Core",loglevelcode.INFO)

        pos=-1
        pos=processor_name.find("I7-")
        if (pos<0): pos=processor_name.find("I5-")
        if (pos<0): pos=processor_name.find("I3-")

        core_vnum=processor_name[pos+3:pos+7]
        try:
            procnum=int(core_vnum)
            archnum=procnum/1000
            if (archnum==4):
		print_info("Processor arch: Haswell",loglevelcode.INFO)
            elif (archnum==5):
		print_info("Processor arch: Broadwell",loglevelcode.INFO)
            elif (archnum==6): 
                print_info("Processor arch: Skylake",loglevelcode.INFO)
        except:
            pass
        

    elif (processor_name.find("XEON")>=0):
	print_info("Processor brand: Xeon",loglevelcode.INFO)
        pos=processor_name.find(" V")
        if pos>0:
	    xeon_vnum=processor_name[pos+1:pos+3]
	    if ("V3" in xeon_vnum):
		print_info("Processor arch: Haswell",loglevelcode.INFO)
            elif ("V4" in xeon_vnum):
		print_info("Processor arch: Broadwell",loglevelcode.INFO)
            elif ("V5" in xeon_vnum): 
                print_info("Processor arch: Skylake",loglevelcode.INFO)

    else:
        print_info("Processor not Xeon or Core.  Not supported.",loglevelcode.ERROR)
    
   

    return loglevelcode.SUCCESS
 
def is_OS_media_ready():

    #check GPU PCIid
    lspci_output=run_cmd("lspci -nn -s 0:02.0")
    pos=lspci_output.rfind("[8086:")
    pciid=lspci_output[pos+6:pos+10].upper()
    (sts,gpustr)=parse_pciid(pciid)
    print_info("GPU PCI id     : " +pciid,loglevelcode.INFO)
    print_info("GPU description: "+gpustr,loglevelcode.INFO)
    if sts==loglevelcode.SUCCESS:
        print_info("GPU visible to OS",loglevelcode.SUCCESS)
    else:
        print_info("No compatible GPU available.  Check BIOS settings?",loglevelcode.INFO)
        return loglevelcode.INFO

    #check for nomodeset
    grub_cmdline_output=run_cmd("cat /proc/cmdline")
    if (grub_cmdline_output.find("nomodeset")>0):
        print_info("nomodeset detected in GRUB cmdline",loglevelcode.ERROR)
        return loglevelcode.ERROR
    else:
        print_info("no nomodeset in GRUB cmdline (good)",loglevelcode.INFO)
        

    #Linux distro
    (linux_distro_name,linux_distro_version,linux_distro_details)=platform.linux_distribution()
    linux_distro=linux_distro_name+" "+linux_distro_version
    print_info("Linux distro   : "+linux_distro,loglevelcode.INFO)

    #kernel
    uname_output=run_cmd("uname -r")
    print_info("Linux kernel   : "+uname_output.strip(),loglevelcode.INFO)

    #glibc version
    ldd_version_output=run_cmd("ldd --version")
    pos=ldd_version_output.find("Copyright")
    ldd_version_output=ldd_version_output[0:pos-1]
    tmp=ldd_version_output.split()

    try:
        ldd_version=float(tmp.pop())
    except:
        ldd_version=0

    if (ldd_version>=2.12):
        outstr="glibc version  : %4.2f"%(ldd_version)
        print_info(outstr,loglevelcode.INFO)
    else:
        outstr="glibc version  : %4.2f >= 2.12 required!"%(ldd_version)
        print_info(outstr,loglevelcode.ERROR)
        return loglevelcode.ERROR

 
    
    if (linux_distro.find("CentOS Linux 7.1.1503")>=0):
        print_info("Linux distro suitable for Media Server Studio 2016 Gold",loglevelcode.SUCCESS)
    else:
        print_info("Linux distro suitable for Generic install",loglevelcode.INFO)

    return loglevelcode.SUCCESS




if __name__ == "__main__":


    if len(sys.argv)>1:
        if (sys.argv[1]=="--help"):
            print "usage: python sys_analyzer_linux.py [-v]"
            print "-v = verbose"

        if (sys.argv[1]=="-v"):
            GLOBAL_LOGLEVEL=2

    #HW media ready: processor,gpu ID (yes,no,advice)
    print "--------------------------"
    print "Hardware readiness checks:"
    print "--------------------------"
    sts=does_processor_have_gen_graphics()
    if (sts<loglevelcode.SUCCESS): sys.exit(1)

    #OS media ready: OS,glibc version,gcc version,nomodeset,gpuID (yes, no, advice, gold/generic)
    print "--------------------------"
    print "OS readiness checks:"
    print "--------------------------"    
    sts=is_OS_media_ready()
    if (sts<loglevelcode.SUCCESS): sys.exit(1)


    #MSS install correctness: vainfo, /dev/dri, check MSDK dirs, check OCL dirs, check MSDK/OCL funcs
    print "--------------------------"
    print "Media Server Studio Install:"
    print "--------------------------"      
    #in video group
    out=run_cmd("groups")
    if ("video" in out):
        print_info("user in video group",loglevelcode.SUCCESS)
    else:
        print_info("user not in video group.  Add with usermod -a -G video {user}",loglevelcode.ERROR)       

    #vainfo: exists,correct iHD used
    out=run_cmd("vainfo 2>&1")
    if ("iHD_drv_video.so" in out):
        print_info("Intel iHD used by libva",loglevelcode.INFO)
    else:
        print_info("libva not loading Intel iHD",loglevelcode.ERROR)
    
    if ("VAEntrypoint" in out):
        print_info("vainfo reports valid codec entry points",loglevelcode.SUCCESS)
    else:
        print_info("vainfo not reporting codec entry points",loglevelcode.ERROR)       

    #check i915 use
    out=run_cmd("lspci -v -s 0:02.0")
    if ("Kernel driver in use: i915" in out):
        print_info("i915 driver in use by Intel video adapter",loglevelcode.INFO)
    else:
        print_info("Intel video adapter not using i915",loglevelcode.ERROR)


    print "------------------------------"
    print "Pls be sure to read README.md "
    print "ALso txt files"
    print "------------------------------"      
