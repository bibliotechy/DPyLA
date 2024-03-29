## Defines searchable fields so that we don' try to search fields that aren't real
searchable_fields = (
    "dataProvider",
    "hasView",
    "hasView.format",
    "hasView.rights",
    "ingestDate",
    "ingestType",
    "isShownAt",
    "isShownAt.@id",
    "isShownAt.format",
    "isShownAt.rights",
    "object",
    "object.@id",
    "object.format",
    "object.rights",
    "originalRecord",
    "provider",
    "provider.@id",
    "provider.name",
    "sourceResource",
    "sourceResource.collection",
    "sourceResource.collection.@id",
    "sourceResource.contributor",
    "sourceResource.creator",
    "sourceResource.date",
    "sourceResource.date.begin",
    "sourceResource.date.displayDate",
    "sourceResource.date.end",
    "sourceResource.description",
    "sourceResource.extent",
    "sourceResource.format",
    "sourceResource.identifier",
    "sourceResource.language",
    "sourceResource.language.name",
    "sourceResource.language.iso639",
    "sourceResource.physicalMedium",
    "sourceResource.publisher",
    "sourceResource.rights",
    "sourceResource.spatial",
    "sourceResource.spatial.coordinates",
    "sourceResource.spatial.city",
    "sourceResource.spatial.county",
    "sourceResource.spatial.distance",
    "sourceResource.spatial.iso3166-2",
    "sourceResource.spatial.name",
    "sourceResource.spatial.region",
    "sourceResource.spatial.state",
    "sourceResource.stateLocatedIn.name",
    "sourceResource.stateLocatedIn.iso3166-2",
    "sourceResource.subject",
    "sourceResource.subject.@id",
    "sourceResource.subject.@type",
    "sourceResource.subject.name",
    "sourceResource.temporal",
    "sourceResource.temporal.begin",
    "sourceResource.temporal.end",
    "sourceResource.title",
    "sourceResource.type",
)
