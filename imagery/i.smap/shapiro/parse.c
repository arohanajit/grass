#include <stdlib.h>
#include <grass/gis.h>
#include <grass/glocale.h>
#include <grass/imagery.h>
#include "bouman.h"


int parse (int argc, char *argv[], struct parms *parms)
{
    struct Option *group, *subgroup, *sigfile, *output;
    struct Option *blocksize;
    struct Flag *quiet;
    struct Flag *ml;

    group = G_define_standard_option(G_OPT_I_GROUP);

    subgroup = G_define_standard_option(G_OPT_I_SUBGROUP);

    sigfile = G_define_option();
    sigfile->key = "signaturefile";
    sigfile->description = _("Name of imagery signaturefile");
    sigfile->key_desc     = "name";
    sigfile->required = YES;
    sigfile->type = TYPE_STRING;

    blocksize = G_define_option();
    blocksize->key = "blocksize";
    blocksize->description = _("Size of submatrix to process at one time");
    blocksize->required = NO;
    blocksize->type = TYPE_INTEGER;
    blocksize->answer = "128";

    output = G_define_standard_option(G_OPT_R_OUTPUT);

    ml = G_define_flag();
    ml->key = 'm';
    ml->description = _("Use maximum likelihood estimation (instead of smap)");

    quiet = G_define_flag();
    quiet->key = 'q';
    quiet->description = _("Run quietly");

    if (G_parser(argc,argv)) exit(EXIT_FAILURE);

    parms->quiet = quiet->answer;
    parms->ml = ml->answer;

    parms->output_map = output->answer;
    parms->group = group->answer;
    parms->subgroup = subgroup->answer;
    parms->sigfile = sigfile->answer;

    /* check all the inputs */
    if (!I_find_group(parms->group))
        G_fatal_error(_("Group [%s] not found."), parms->group);

    if (!I_find_subgroup(parms->group, parms->subgroup))
        G_fatal_error(_("Subgroup [%s] not found."), parms->subgroup);

    if (sscanf(blocksize->answer,"%d",&parms->blocksize) !=1
    || parms->blocksize <= 8) parms->blocksize = 8;

    return 0;
}
