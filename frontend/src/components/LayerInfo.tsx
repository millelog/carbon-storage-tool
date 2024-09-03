import React from 'react';
import {
  Card,
  CardContent,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { ScrollArea } from "@/components/ui/scroll-area";

interface LayerSchema {
  name: string;
  properties: string[];
}

interface LayerInfoProps {
  schema: LayerSchema;
}

const LayerInfo: React.FC<LayerInfoProps> = ({ schema }) => {
  return (
    <Card className="w-full max-w-md mx-auto bg-white shadow-md">
      <CardContent className="p-0">
        <Accordion type="single" collapsible defaultValue="layer-info" className="w-full">
          <AccordionItem value="layer-info">
            <AccordionTrigger className="px-4 py-2 bg-gray-100 hover:bg-gray-200 transition-colors">
              <span className="text-lg font-semibold text-gray-800">{schema.name}</span>
            </AccordionTrigger>
            <AccordionContent>
              <div className="p-4">
                <h3 className="text-sm font-medium text-gray-600 mb-2">Properties:</h3>
                <ScrollArea className="h-[200px] w-full rounded-md border border-gray-200 p-4">
                  <div className="flex flex-wrap gap-2">
                    {schema.properties.map((prop, index) => (
                      <Badge key={index} variant="secondary" className="bg-blue-100 text-blue-800 hover:bg-blue-200">
                        {prop}
                      </Badge>
                    ))}
                  </div>
                </ScrollArea>
              </div>
            </AccordionContent>
          </AccordionItem>
        </Accordion>
      </CardContent>
    </Card>
  );
};

export default LayerInfo;