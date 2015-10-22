"""
mtbtn module. Contains the Mt3dBtn class. Note that the user can access
the Mt3dBtn class as `flopy.mt3d.Mt3dBtn`.

Additional information for this MT3DMS package can be found in the MT3DMS
User's Manual.

"""

import numpy as np
# from numpy import empty,array
from flopy.mbase import Package
from flopy.utils import util_2d, util_3d, read1d


class Mt3dBtn(Package):
    """
    Basic Transport Package Class.

    Parameters
    ----------
    model : model object
        The model object (of type :class:`flopy.mt3dms.mt.Mt3dms`) to which
        this package will be added.
    ncomp : int
        The total number of chemical species in the simulation. (default is
        None, will be changed to 1 if sconc is single value)
    mcomp : int
        The total number of 'mobile' species (default is 1). mcomp must be
        equal or less than ncomp.
    tunit : str
        The name of unit for time (default is 'D', for 'days'). Used for
        identification purposes only.
    lunit : str
        The name of unit for length (default is 'M', for 'meters'). Used for
        identification purposes only.
    munit : str
        The name of unit for mass (default is 'KG', for 'kilograms'). Used for
        identification purposes only.
    prsity : float or array of floats (nlay, nrow, ncol)
        The effective porosity of the porous medium in a single porosity
        system, or the mobile porosity in a dual-porosity medium (the immobile
        porosity is defined through the Chemical Reaction Package. (default is
        0.25).
    icbund : int or array of ints (nlay, nrow, ncol)
        The icbund array specifies the boundary condition type for solute
        species (shared by all species). If icbund = 0, the cell is an inactive
        concentration cell; If icbund < 0, the cell is a constant-concentration
        cell; If icbund > 0, the cell is an active concentration cell where the
        concentration value will be calculated. (default is 1).
    sconc : float, array of (nlay, nrow, ncol), or filename, or a list (length
            ncomp) of these for multi-species simulations
        The starting concentration for the solute transport simulation.
    cinact : float
        The value for indicating an inactive concentration cell. (default is
        1e30).
    thkmin : float
        The minimum saturated thickness in a cell, expressed as the decimal
        fraction of its thickness, below which the cell is considered inactive.
        (default is 0.01).
    ifmtcn : int
        A flag/format code indicating how the calculated concentration should
        be printed to the standard output text file. Format codes for printing
        are listed in Table 3 of the MT3DMS manual. If ifmtcn > 0 printing is
        in wrap form; ifmtcn < 0 printing is in strip form; if ifmtcn = 0
        concentrations are not printed. (default is 0).
    ifmtnp : int
        A flag/format code indicating how the number of particles should
        be printed to the standard output text file. The convention is
        the same as for ifmtcn. (default is 0).
    ifmtrf : int
        A flag/format code indicating how the calculated retardation factor
        should be printed to the standard output text file. The convention is
        the same as for ifmtcn. (default is 0).
    ifmtdp : int
        A flag/format code indicating how the distance-weighted dispersion
        coefficient should be printed to the standard output text file. The
        convention is the same as for ifmtcn. (default is 0).
    savucn : bool
        A logical flag indicating whether the concentration solution should be
        saved in an unformatted file. (default is True).
    nprs : int
        A flag indicating (i) the frequency of the output and
        (ii) whether the output frequency is specified in terms
        of total elapsed simulation time or the transport step number. If
        nprs > 0 results will be saved at the times as specified in timprs;
        if nprs = 0, results will not be saved except at the end of simulation;
        if NPRS < 0, simulation results will be saved whenever the number of
        transport steps is an even multiple of nprs. (default is 0).
    timprs : list of floats
        The total elapsed time at which the simulation results are saved. The
        number of entries in timprs must equal nprs. (default is None).
    obs: array of int
        An array with the cell indices (layer, row, column) for which the
        concentration is to be printed at every transport step. (default is
        None).
    nprobs: int
        An integer indicating how frequently the concentration at the specified
        observation points should be saved. (default is 1).
    chkmas: bool
        A logical flag indicating whether a one-line summary of mass balance
        information should be printed. (default is True).
    nprmas: int
        An integer indicating how frequently the mass budget information
        should be saved. (default is 1).
    dt0: float
        The user-specified initial transport step size within each time-step 
        of the flow solution. (default is 0).
    mxstrn: int
        The maximum number of transport steps allowed within one time step
        of the flow solution. (default is 50000).
    ttsmult: float
        The multiplier for successive transport steps within a flow time-step
        if the GCG solver is used and the solution option for the advection
        term is the standard finite-difference method. (default is 1.0).
    ttsmax: float
        The maximum transport step size allowed when transport step size
        multiplier TTSMULT > 1.0. (default is 0).
    species_names: list of str
        A list of names for every species in the simulation.
    extension : string
        Filename extension (default is 'btn')

    Attributes
    ----------

    Methods
    -------

    See Also
    --------

    Notes
    -----

    Examples
    --------

    >>> import flopy
    >>> mt = flopy.mt3dms.Mt3dms()
    >>> btn = flopy.mt3dms.Mt3dBtn(mt)

    """
    unitnumber = 31
    def __init__(self, model, ncomp=1, mcomp=1, tunit='D', lunit='M',
                 munit='KG', prsity=0.30, icbund=1, sconc=0.0,
                 cinact=1e30, thkmin=0.01, ifmtcn=0, ifmtnp=0,
                 ifmtrf=0, ifmtdp=0, savucn=True, nprs=0, timprs=None,
                 obs=None, nprobs=1, chkmas=True, nprmas=1, dt0=0,
                 mxstrn=50000, ttsmult=1.0, ttsmax=0,
                 species_names=[], extension='btn', **kwargs):
        Package.__init__(self, model, extension, 'BTN', self.unitnumber)
        nrow, ncol, nlay, nper = self.parent.mf.nrow_ncol_nlay_nper
        self.heading1 = '# BTN for MT3DMS, generated by Flopy.'
        self.heading2 = '#'
        self.mcomp = mcomp
        self.tunit = tunit
        self.lunit = lunit
        self.munit = munit
        self.cinact = cinact
        self.thkmin = thkmin
        self.ifmtcn = ifmtcn
        self.ifmtnp = ifmtnp
        self.ifmtrf = ifmtrf
        self.ifmtdp = ifmtdp
        self.savucn = savucn
        self.nprs = nprs
        self.timprs = timprs
        self.obs = obs
        self.nprobs = nprobs
        self.chkmas = chkmas
        self.nprmas = nprmas
        self.species_names = species_names
        self.prsity = util_3d(model, (nlay, nrow, ncol), np.float32,
                              prsity, name='prsity', locat=self.unit_number[0])
        self.__icbund = util_3d(model, (nlay, nrow, ncol), np.int,
                                icbund, name='icbund',
                                locat=self.unit_number[0])
        # Starting concentrations
        # some defense
        #
        self.ncomp = ncomp
        self.sconc = []
        u3d = util_3d(model, (nlay, nrow, ncol), np.float32, sconc,
                      name='sconc1', locat=self.unit_number[0])
        self.sconc.append(u3d)
        if ncomp > 1:
            for icomp in range(2, ncomp + 1):
                name = "sconc" + str(icomp)
                val = 0.0
                if name in list(kwargs.keys()):
                    val = kwargs[name]
                    kwargs.pop(name)
                else:
                    print("BTN: setting sconc for component " + \
                          str(icomp) + " to zero, kwarg name " + \
                          name)

                u3d = util_3d(model, (nlay, nrow, ncol), np.float32,
                              val, name=name,
                              locat=self.unit_number[0])
                self.sconc.append(u3d)
        if len(list(kwargs.keys())) > 0:
            raise Exception("BTN error: unrecognized kwargs: " +
                            ' '.join(list(kwargs.keys())))
        self.dt0 = util_2d(model, (nper,), np.float32, dt0, name='dt0')
        self.mxstrn = util_2d(model, (nper,), np.int, mxstrn, name='mxstrn')
        self.ttsmult = util_2d(model, (nper,), np.float32, ttsmult,
                               name='ttmult')
        self.ttsmax = util_2d(model, (nper,), np.float32, ttsmax, name='ttsmax')
        self.parent.add_package(self)

    def geticbund(self):
        """
        Return the icbund array.

        Returns
        -------
        icbund : numpy.ndarray (nlay, nrow, ncol)
            icbund object.
        """
        return self.__icbund.array

    def seticbund(self, icbund):
        """
        Set the icbund array.
        """
        model = self.parent
        nrow, ncol, nlay, nper = model.nrow_ncol_nlay_nper
        self.__icbund = util_3d(model, (nlay, nrow, ncol), np.int, icbund,
                                name='icbund', locat=self.unit_number[0])
        return

    icbund = property(geticbund, seticbund)

    def write_file(self):
        nrow, ncol, nlay, nper = self.parent.mf.nrow_ncol_nlay_nper
        ModflowDis = self.parent.mf.get_package('DIS')
        # Open file for writing
        f_btn = open(self.fn_path, 'w')
        f_btn.write('#{0:s}\n#{1:s}\n'.format(self.heading1, self.heading2))
        f_btn.write('{0:10d}{1:10d}{2:10d}{3:10d}{4:10d}{5:10d}\n'
                    .format(nlay, nrow, ncol, nper, self.ncomp, self.mcomp))
        f_btn.write('{0:4s}{1:4s}{2:4s}\n' \
                    .format(self.tunit, self.lunit, self.munit))
        if (self.parent.adv != None):
            f_btn.write('{0:2s}'.format('T'))
        else:
            f_btn.write('{0:2s}'.format('F'))
        if (self.parent.dsp != None):
            f_btn.write('{0:2s}'.format('T'))
        else:
            f_btn.write('{0:2s}'.format('F'))
        if (self.parent.ssm != None):
            f_btn.write('{0:2s}'.format('T'))
        else:
            f_btn.write('{0:2s}'.format('F'))
        if (self.parent.rct != None):
            f_btn.write('{0:2s}'.format('T'))
        else:
            f_btn.write('{0:2s}'.format('F'))
        if (self.parent.gcg != None):
            f_btn.write('{0:2s}'.format('T'))
        else:
            f_btn.write('{0:2s}'.format('F'))
        f_btn.write('\n')
        flow_package = self.parent.mf.get_package('BCF6')
        if (flow_package != None):
            lc = util_2d(self.parent, (nlay,), np.int,
                         flow_package.laycon.get_value(),
                         name='btn - laytype',
                         locat=self.unit_number[0])
        else:
            flow_package = self.parent.mf.get_package('LPF')
            if (flow_package != None):
                lc = util_2d(self.parent, (nlay,),
                             np.int, flow_package.laytyp.get_value(),
                             name='btn - laytype', locat=self.unit_number[0])
        # need to reset lc fmtin
        lc.set_fmtin('(40I2)')
        f_btn.write(lc.string)
        delr = util_2d(self.parent, (ncol,),
                       np.float32, ModflowDis.delr.get_value(),
                       name='delr', locat=self.unit_number[0])
        f_btn.write(delr.get_file_entry())

        delc = util_2d(self.parent, (nrow,), np.float32,
                       ModflowDis.delc.get_value(), name='delc',
                       locat=self.unit_number[0])
        f_btn.write(delc.get_file_entry())

        top = util_2d(self.parent, (nrow, ncol),
                      np.float32, ModflowDis.top.array,
                      name='top', locat=self.unit_number[0])
        f_btn.write(top.get_file_entry())

        thickness = util_3d(self.parent, (nlay, nrow, ncol),
                            np.float32, ModflowDis.thickness.get_value(),
                            name='thickness', locat=self.unit_number[0])
        f_btn.write(thickness.get_file_entry())

        f_btn.write(self.prsity.get_file_entry())

        f_btn.write(self.__icbund.get_file_entry())

        # Starting concentrations
        for s in range(len(self.sconc)):
            f_btn.write(self.sconc[s].get_file_entry())

        f_btn.write('{0:10.0E}{1:10.4f}\n' \
                    .format(self.cinact, self.thkmin))

        f_btn.write('{0:10d}{1:10d}{2:10d}{3:10d}' \
                    .format(self.ifmtcn, self.ifmtnp, self.ifmtrf, self.ifmtdp))
        if (self.savucn == True):
            ss = 'T'
        else:
            ss = 'F'
        f_btn.write('{0:>10s}\n'.format(ss))

        # NPRS
        if (self.timprs == None):
            f_btn.write('{0:10d}\n'.format(self.nprs))
        else:
            f_btn.write('{0:10d}\n'.format(len(self.timprs)))
            timprs = util_2d(self.parent, (len(self.timprs),),
                             np.float32, self.timprs, name='timprs',
                             fmtin='(8G10.4)')
            f_btn.write(timprs.string)
        # OBS
        if (self.obs == None):
            f_btn.write('{0:10d}{1:10d}\n'.format(0, self.nprobs))
        else:
            nobs = self.obs.shape[0]
            f_btn.write('{0:10d}{1:10d}\n'.format(nobs, self.nprobs))
            for r in range(nobs):
                f_btn.write('{0:10d}{1:10d}{2:10d}\n' \
                            .format(self.obs[r, 0], self.obs[r, 1], self.obs[r, 2]))
        # CHKMAS, NPRMAS
        if (self.chkmas == True):
            ss = 'T'
        else:
            ss = 'F'
        f_btn.write('{0:>10s}{1:10d}\n'.format(ss, self.nprmas))
        # PERLEN, NSTP, TSMULT
        for t in range(nper):
            f_btn.write('{0:10.4G}{1:10d}{2:10.4G}\n'
                        .format(ModflowDis.perlen[t], ModflowDis.nstp[t],
                                ModflowDis.tsmult[t]))
            f_btn.write('{0:10.4G}{1:10d}{2:10.4G}{3:10.4G}\n'
                        .format(self.dt0[t], self.mxstrn[t],
                                self.ttsmult[t], self.ttsmax[t]))
        f_btn.close()

    @staticmethod
    def load(f, model, nlay=None, nrow=None, ncol=None, ext_unit_dict=None):
        if not hasattr(f, 'read'):
            filename = f
            f = open(filename, 'r')

        # A1
        if model.verbose:
            print('   loading COMMENT LINES A1 AND A2...')
        line = f.readline()
        if model.verbose:
            print('A1: '.format(line.strip()))

        # A2
        line = f.readline()
        if model.verbose:
            print('A2: '.format(line.strip()))

        # A3
        if model.verbose:
            print('   loading NLAY, NROW, NCOL, NPER, NCOMP, MCOMP...')
        line = f.readline()
        nlay = int(line[0:10])
        nrow = int(line[11:20])
        ncol = int(line[21:30])
        nper = int(line[31:40])
        ncomp = int(line[41:50])
        mcomp = int(line[51:60])
        if model.verbose:
            print('   NLAY {}'.format(nlay))
            print('   NROW {}'.format(nrow))
            print('   NCOL {}'.format(ncol))
            print('   NPER {}'.format(nper))
            print('   NCOMP {}'.format(ncomp))
            print('   MCOMP {}'.format(mcomp))

        if ncomp > 1:
            raise NotImplementedError("BTN.load() doesn't support ncomp > 1")

        if model.verbose:
            print('   loading TUNIT, LUNIT, MUNIT...')
        line = f.readline()
        tunit = line[0:4]
        lunit = line[4:8]
        munit = line[8:12]
        if model.verbose:
            print('   TUNIT {}'.format(tunit))
            print('   LUNIT {}'.format(lunit))
            print('   MUNIT {}'.format(munit))

        if model.verbose:
            print('   loading TRNOP...')
        trnop = f.readline().strip().split()
        if model.verbose:
            print('   TRNOP {}'.format(trnop))

        if model.verbose:
            print('   loading LAYCON...')
        laycon = np.empty((nlay), np.int)
        laycon = read1d(f, laycon)
        if model.verbose:
            print('   LAYCON {}'.format(laycon))

        if model.verbose:
            print('   loading DELR...')
        delr = util_2d.load(f, model, (ncol, 1), np.float32, 'delr',
                            ext_unit_dict)
        if model.verbose:
            print('   DELR {}'.format(delr))

        if model.verbose:
            print('   loading DELC...')
        delc = util_2d.load(f, model, (nrow, 1), np.float32, 'delc',
                            ext_unit_dict)
        if model.verbose:
            print('   DELC {}'.format(delc))

        if model.verbose:
            print('   loading HTOP...')
        htop = util_2d.load(f, model, (nrow, ncol), np.float32, 'htop',
                            ext_unit_dict)
        if model.verbose:
            print('   HTOP {}'.format(htop))

        if model.verbose:
            print('   loading DZ...')
        dz = util_3d.load(f, model, (nlay, nrow, ncol), np.float32, 'dz',
                          ext_unit_dict)
        if model.verbose:
            print('   DZ {}'.format(dz))

        if model.verbose:
            print('   loading PRSITY...')
        prsity = util_3d.load(f, model, (nlay, nrow, ncol), np.float32, 'prsity',
                              ext_unit_dict)
        if model.verbose:
            print('   PRSITY {}'.format(prsity))

        if model.verbose:
            print('   loading ICBUND...')
        icbund = util_3d.load(f, model, (nlay, nrow, ncol), np.int, 'icbund',
                              ext_unit_dict)
        if model.verbose:
            print('   ICBUND {}'.format(icbund))

        if model.verbose:
            print('   loading SCONC...')
        sconc = util_3d.load(f, model, (nlay, nrow, ncol), np.float32, 'sconc',
                             ext_unit_dict)
        if model.verbose:
            print('   SCONC {}'.format(sconc))

        if model.verbose:
            print('   loading CINACT, THCKMIN...')
        line = f.readline()
        cinact = float(line[0:10])
        try:
            thkmin = float(line[10:20])
        except:
            thkmin = 0.01
        if model.verbose:
            print('   CINACT {}'.format(cinact))
            print('   THKMIN {}'.format(thkmin))

        if model.verbose:
            print('   loading IFMTCN, IFMTNP, IFMTRF, IFMTDP, SAVUCN...')
        line = f.readline()
        ifmtcn = int(line[0:10])
        ifmtnp = int(line[10:20])
        ifmtrf = int(line[20:30])
        ifmtdp = int(line[30:40])
        savucn = False
        if 't' in line[40:50].lower():
            savucn = True
        if model.verbose:
            print('   IFMTCN {}'.format(ifmtcn))
            print('   IFMTNP {}'.format(ifmtnp))
            print('   IFMTRF {}'.format(ifmtrf))
            print('   IFMTDP {}'.format(ifmtdp))
            print('   SAVUCN {}'.format(savucn))

        if model.verbose:
            print('   loading NPRS...')
        line = f.readline()
        nprs = int(line[0:10])
        if model.verbose:
            print('   NPRS {}'.format(nprs))

        timprs = None
        if nprs > 0:
            if model.verbose:
                print('   loading TIMPRS...')
            timprs = np.empty((nprs), dtype=np.float32)
            read1d(f, timprs)
            if model.verbose:
                print('   TIMPRS {}'.format(timprs))

        if model.verbose:
            print('   loading NOBS, NPROBS...')
        line = f.readline()
        nobs = int(line[0:10])
        try:
            nprobs = int(line[10:20])
        except:
            nprobs = 1
        if model.verbose:
            print('   NOBS {}'.format(nobs))
            print('   NPROBS {}'.format(nprobs))

        if nobs > 0:
            if model.verbose:
                print('   loading KOBS, IOBS, JOBS...')
            obs = []
            for l in range(nobs):
                line = f.readline()
                k = int(line[0:10])
                i = int(line[10:20])
                j = int(line[20:30])
                obs.append([k, i, j])
            obs = np.array(obs)
            if model.verbose:
                print('   OBS {}'.format(obs))

        if model.verbose:
            print('   loading CHKMAS, NPRMAS...')
        line = f.readline()
        chkmas = False
        if 't' in line[0:10].lower():
            chkmas = True
        try:
            nprmas = int(line[10:20])
        except:
            nprmas = 1
        if model.verbose:
            print('   CHKMAS {}'.format(chkmas))
            print('   NPRMAS {}'.format(nprmas))


        if model.verbose:
            print('   loading PERLEN, NSTP, TSMULT, TSLNGH, DT0, MXSTRN, TTSMULT, TTSMAX...')
        dt0, mxstrn, ttsmult, ttsmax = [], [], [], []
        perlen = []
        nstp = []
        tsmult = []
        tslngh = []
        for kper in range(nper):
            line = f.readline()
            perlen.append(float(line[0:10]))
            nstp.append(int(line[10:20]))
            tsmult.append(float(line[20:30]))

            if tsmult[-1] < 0:
                t = np.empty((nstp[-1]), dtype=np.float32)
                read1d(f, t)
                tslngh.append(t)
                raise Exception("tsmult <= 0 not supported")

            line = f.readline()
            dt0.append(float(line[0:10]))
            mxstrn.append(int(line[10:20]))
            ttsmult.append(float(line[20:30]))
            ttsmax.append(float(line[30:40]))
        if model.verbose:
            print('   PERLEN {}'.format(perlen))
            print('   NSTP {}'.format(nstp))
            print('   TSMULT {}'.format(tsmult))
            print('   TSLNGH {}'.format(tslngh))
            print('   DT0 {}'.format(dt0))
            print('   MXSTRN {}'.format(mxstrn))
            print('   TTSMULT {}'.format(ttsmult))
            print('   TTSMAX {}'.format(ttsmax))

        # Close the file
        f.close()

        btn = Mt3dBtn(model, ncomp=ncomp, mcomp=mcomp, tunit=tunit,
                      lunit=lunit, munit=munit, prsity=prsity, icbund=icbund,
                      sconc=sconc, cinact=cinact, thkmin=thkmin,
                      ifmtcn=ifmtcn, ifmtnp=ifmtnp, ifmtrf=ifmtrf,
                      ifmtdp=ifmtdp, savucn=savucn, nprs=nprs,
                      timprs=timprs, obs=obs, nprobs=nprobs, chkmas=chkmas,
                      nprmas=nprmas, dt0=dt0, mxstrn=mxstrn, ttsmult=ttsmult,
                      ttsmax=ttsmax)
        return btn
